# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long
"""Visit CSAF/CVRF files and validate them against envelope (core) and given body profiles."""
import copy
import csv
import datetime as dti
import hashlib
import json
import lzma
import os
import pathlib
import subprocess
import sys

import jsonschema  # type: ignore
from lxml import etree  # type: ignore


ENCODING = "utf-8"

CSAF_DEFAULT_SEMANTIC_VERSION = '2.0'
CRVF_DEFAULT_SEMANTIC_VERSION = '1.2'
CRVF_PRE_OASIS_SEMANTIC_VERSION = '1.1'
CRVF_KNOWN_SEMANTIC_VERSIONS = (CRVF_DEFAULT_SEMANTIC_VERSION, CRVF_PRE_OASIS_SEMANTIC_VERSION)
CVRF_PARTS = ('cvrf', 'vuln', 'prod')
CSAF_2_0_SCHEMA_PATH = pathlib.Path('csaf_lint', 'schema', 'csaf', CSAF_DEFAULT_SEMANTIC_VERSION, 'csaf.json')

CVRF_OASIS_ROOT = 'http://docs.oasis-open.org/csaf/csaf-cvrf/'

CVRF_DEFAULT_SCHEMA = f'{CVRF_OASIS_ROOT}v{CRVF_DEFAULT_SEMANTIC_VERSION}/cs01/schemas/cvrf.xsd'
CVRF_DEFAULT_NAMESPACES = {part.upper(): '{{{CVRF_OASIS_ROOT}v{CRVF_DEFAULT_SEMANTIC_VERSION}/{part}}}' for part in CVRF_PARTS}

CVRF_DEFAULT_CATALOG = pathlib.Path('csaf_lint', 'schema', f'catalog_{CRVF_DEFAULT_SEMANTIC_VERSION.replace(".", "_")}.xml')
CVRF_DEFAULT_SCHEMA_FILE = pathlib.Path('csaf_lint', 'schema', 'cvrf', f'{CRVF_DEFAULT_SEMANTIC_VERSION}/cvrf.xsd')

CVRF_PRE_OASIS_ROOT = 'http://www.icasi.org/CVRF/schema/cvrf/'

CVRF_PRE_OASIS_SCHEMA = f'{CVRF_PRE_OASIS_ROOT}{CRVF_PRE_OASIS_SEMANTIC_VERSION}/cs01/schemas/cvrf.xsd'
CVRF_PRE_OASIS_NAMESPACES = {part.upper(): '{{{CVRF_OASIS_ROOT}v{CRVF_DEFAULT_SEMANTIC_VERSION}/{part}}}' for part in CVRF_PARTS}

CVRF_PRE_OASIS_CATALOG = pathlib.Path('csaf_lint', 'schema', f'catalog_{CRVF_PRE_OASIS_SEMANTIC_VERSION.replace(".", "_")}.xml')
CVRF_PRE_OASIS_SCHEMA_FILE = pathlib.Path('csaf_lint', 'schema', 'cvrf', f'{CRVF_PRE_OASIS_SEMANTIC_VERSION}/cvrf.xsd')

CVRF_OASIS_NS_ROOT = 'http://docs.oasis-open.org/csaf/ns/csaf-cvrf/'
CVRF_VERSION_NS_MAP = {
    '1.2': f'{CVRF_OASIS_NS_ROOT}v1.2/cvrf',
    '1.1': f'{CVRF_OASIS_NS_ROOT}v1.1/cvrf',
}

CVRF_VERSION_CATALOG_MAP = {
    '1.2': CVRF_DEFAULT_CATALOG,
    '1.1': CVRF_PRE_OASIS_CATALOG,
}

DEBUG_VAR = "CSL_DEBUG"
DEBUG = os.getenv(DEBUG_VAR)


def read_stdin():
    """Create JSON object from stdin data."""
    in_memory = [line for line in sys.stdin]
    return json.loads(''.join(in_memory))


def load(file_path):
    """Create JSON object from file."""
    with open(file_path, "rt", encoding=ENCODING) as handle:
        return json.load(handle)


def version_from(schema_path):
    """HACK A DID ACK derives non-default 1.1 version from path."""
    if CRVF_PRE_OASIS_SEMANTIC_VERSION in str(schema_path):
        return CRVF_PRE_OASIS_SEMANTIC_VERSION
    return CRVF_DEFAULT_SEMANTIC_VERSION


def validate(document, schema, conformance=None):
    """Validate the document against the schema."""
    if isinstance(document, dict):  # HACK A DID ACK
        conformance = conformance if conformance else jsonschema.draft7_format_checker
        return jsonschema.validate(document, schema, format_checker=conformance)
    xml_tree, message = load_xml(document)
    if not xml_tree:
        print(message)
        return 1
    request_version = version_from(schema)
    DEBUG and print(f"DEBUG>>> {schema=}, {request_version=}")
    found, version, ns = versions_xml(xml_tree, request_version)
    DEBUG and print(f"DEBUG>>> {found=}, {version=}, {ns=}")
    catalog = CVRF_VERSION_CATALOG_MAP[request_version]
    DEBUG and print(f"DEBUG>>> caller site validation: {schema=}, {catalog=}, {xml_tree=}, {request_version=}")
    status, message = xml_validate(schema, catalog, xml_tree, request_version)
    if not DEBUG and not status:
        print(message)
    DEBUG and print(f"DEBUG>>> {status=}, {message=}")
    return None if status else 1


def load_xml(document_path):
    """
    First things first: parse the document (to ensure it is well-formed XML) to obtain an ElementTree object
    to pass to the CVRF validator/parser
    """
    try:
        cvrf_doc = etree.parse(document_path, etree.XMLParser(encoding="utf-8"))  # "utf-8"
    except IOError as err:
        return None, f"file {document_path} failed with IO error {err}"
    except etree.XMLSyntaxError as err:
        return None, f"parsing from {document_path} failed with XMLSyntaxError error {err}"

    return cvrf_doc, f"well-formed xml tree from {document_path}"


def derive_version_from_namespace(root):
    """Version detection of XML document per element tree object root."""
    not_found = '', None
    if root is None:
        return not_found

    mandatory_element = 'DocumentType'
    for version, ns in CVRF_VERSION_NS_MAP.items():
        token = '{%s}%s' % (ns, mandatory_element)
        if root.find(token) is not None:
            return version, ns

    return not_found


def versions_xml(xml_tree, request_version):
    """Versions from cvrf namespace in xml tree and request version."""
    sem_ver, doc_cvrf_version = derive_version_from_namespace(xml_tree.getroot())
    req_cvrf_version = f"http://docs.oasis-open.org/csaf/ns/csaf-cvrf/v{request_version}/cvrf"

    if doc_cvrf_version:
        return (True if doc_cvrf_version == req_cvrf_version else False), doc_cvrf_version, req_cvrf_version

    return False, None, req_cvrf_version


def cvrf_validate(f, xml_tree):
    """
    Validates a CVRF document

    f: file object containing the schema
    cvrf_doc: the serialized CVRF ElementTree object
    returns: a code (True for valid / False for invalid) and a reason for the code
    """
    try:
        xmlschema_doc = etree.parse(f)
    except etree.XMLSyntaxError as err:
        return False, f'Parsing error, schema document "{f.name}" is not well-formed: {err}'
    xmlschema = etree.XMLSchema(xmlschema_doc)

    try:
        xmlschema.assertValid(xml_tree)
        return True, "Valid"
    except etree.DocumentInvalid:
        return False, xmlschema.error_log


def xml_validate(schema, catalog, xml_tree, request_version):
    """Validate xml tree against given xml schema of request version assisted by catalog."""
    DEBUG and print(f"DEBUG>>> parameters: {schema=}, {catalog=}, {xml_tree=}, {request_version=}")
    fallback_catalog = CVRF_DEFAULT_CATALOG
    if request_version != CRVF_DEFAULT_SEMANTIC_VERSION:
        fallback_catalog = CVRF_PRE_OASIS_CATALOG
    catalog = catalog if catalog else fallback_catalog
    try:
        if schema:
            # Try to use local schema files
            f = open(schema, 'r')

            # If the supplied file is not a valid catalog.xml or doesn't exist lxml will fall back to using remote validation
            os.environ.update(XML_CATALOG_FILES=str(catalog))
        else:
            # try to use local schema file
            fallback_schema = CVRF_DEFAULT_SCHEMA_FILE
            if request_version != CRVF_DEFAULT_SEMANTIC_VERSION:
                fallback_schema = CVRF_PRE_OASIS_SCHEMA_FILE
            schema = fallback_schema
            f = open(schema, 'r')

            catalog = catalog if catalog else fallback_catalog
            os.environ.update(XML_CATALOG_FILES=str(catalog))

    except IOError as err:
        return False, f"validation of {xml_tree} against {schema} failed with IO error: {err}"
    DEBUG and print(f"DEBUG>>> {catalog=}, {schema=}")

    code, result = cvrf_validate(f, xml_tree)
    f.close()

    if code is False:
        return False, f"validation of {xml_tree} against {schema} failed with error: {result}"
    else:
        return True, f"validation of {xml_tree} against {schema} succeeded with result: {result}"


def main(argv=None, embedded=False):
    """Drive the validator."""
    argv = argv if argv else sys.argv[1:]
    if len(argv) > 2:  # Unclear what the inputs beyond two may be
        print("Usage: csaf-lint [schema.json] document.json")
        print("   or: csaf-lint < document.json")
        return 2

    # HACK A DID ACK
    document, schema = '', ''
    if len(argv) and str(argv[-1]).endswith('json'):
        if len(argv) == 2:  # Schema file path is first
            schema = json.loads(argv[0]) if embedded else load(argv[0])
            document = json.loads(argv[1]) if embedded else load(argv[1])
        else:
            schema = load(CSAF_2_0_SCHEMA_PATH)
            if len(argv) == 1:  # Assume schema implicit, argument given is document file path
                document = load(argv[0])
            else:
                document = read_stdin()
    elif len(argv) and str(argv[-1]).endswith('xml'):
        if embedded:
            print("Usage: csaf-lint [schema.xsd] document.xml")
            print(" note: no embedding supported for xsd/xml")
            return 2
        if len(argv) == 2:  # Schema file path is first
            schema = argv[0]
            document = argv[1]
        else:
            schema = CVRF_DEFAULT_SCHEMA_FILE
            if len(argv) == 1:  # Assume schema implicit, argument given is document file path
                document = argv[0]
            else:
                print("Usage: csaf-lint [schema.xsd] document.xml")
                print(" note: no embedding supported for xsd/xml")
                return 2

    return 0 if validate(document, schema) is None else 1
