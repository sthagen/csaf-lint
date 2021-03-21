# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long
"""Visit CSAF/CVRF files and validate them against envelope (core) and given body profiles."""
import json
import os
import pathlib
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
    CRVF_DEFAULT_SEMANTIC_VERSION: f'{CVRF_OASIS_NS_ROOT}v1.2/cvrf',
    CRVF_PRE_OASIS_SEMANTIC_VERSION: f'{CVRF_OASIS_NS_ROOT}v1.1/cvrf',
}

CVRF_VERSION_SCHEMA_MAP = {
    CRVF_DEFAULT_SEMANTIC_VERSION: CVRF_DEFAULT_SCHEMA_FILE,
    CRVF_PRE_OASIS_SEMANTIC_VERSION: CVRF_PRE_OASIS_SCHEMA_FILE,
}

CVRF_VERSION_CATALOG_MAP = {
    CRVF_DEFAULT_SEMANTIC_VERSION: CVRF_DEFAULT_CATALOG,
    CRVF_PRE_OASIS_SEMANTIC_VERSION: CVRF_PRE_OASIS_CATALOG,
}

DEBUG_VAR = "CSL_DEBUG"
DEBUG = os.getenv(DEBUG_VAR)


def read_stdin():
    """Create document from stdin data."""
    DEBUG and print("DEBUG>>> call site loading from stdin")
    return sys.stdin.read()


def load(file_path):
    """Create JSON object from file."""
    DEBUG and print(f"DEBUG>>> call site file loading {file_path=}")
    with open(file_path, "rt", encoding=ENCODING) as handle:
        return json.load(handle)


def version_peek(document_path):
    """HACK A DID ACK derives schema version from reading the first lines from path.
    Something like:

    <?xml version="1.0" encoding="UTF-8"?>
    <cvrfdoc xmlns="http://www.icasi.org/CVRF/schema/cvrf/1.1" xmlns:cvrf="http://www.icasi.org/CVRF/schema/cvrf/1.1">

    or (in addition should work with <cvrf:cvrfdoc style xml documents):

    <?xml version="1.0" encoding="UTF-8"?>
    <cvrfdoc
      xmlns:xsd="http://www.w3.org/2001/XMLSchema"
      xmlns:cpe="http://cpe.mitre.org/language/2.0"
      xmlns:cvrf="http://docs.oasis-open.org/csaf/ns/csaf-cvrf/v1.2/cvrf"
      xmlns:cvrf-common="http://docs.oasis-open.org/csaf/ns/csaf-cvrf/v1.2/common"
      xmlns:cvssv2="http://scap.nist.gov/schema/cvss-v2/1.0"
      xmlns:cvssv3="https://www.first.org/cvss/cvss-v3.0.xsd"
      xmlns:dc="http://purl.org/dc/elements/1.1/"
      xmlns:ns0="http://purl.org/dc/elements/1.1/"
      xmlns:prod="http://docs.oasis-open.org/csaf/ns/csaf-cvrf/v1.2/prod"
      xmlns:scap-core="http://scap.nist.gov/schema/scap-core/1.0"
      xmlns:sch="http://purl.oclc.org/dsdl/schematron"
      xmlns:vuln="http://docs.oasis-open.org/csaf/ns/csaf-cvrf/v1.2/vuln"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xmlns="http://docs.oasis-open.org/csaf/ns/csaf-cvrf/v1.2/cvrf"
      >
    """
    DEBUG and print(f"DEBUG>>> version peek cheap detect on path string {document_path=}")
    if CRVF_PRE_OASIS_SEMANTIC_VERSION in str(document_path):
        return CRVF_PRE_OASIS_SEMANTIC_VERSION
    if CRVF_DEFAULT_SEMANTIC_VERSION in str(document_path):
        return CRVF_DEFAULT_SEMANTIC_VERSION

    DEBUG and print(f"DEBUG>>> version peek naive but deep detect on path content {document_path=}")
    cvrf_element_start = '<cvrf'
    cvrf_element_end = '>'
    naive = []
    with open(document_path) as handle:
        for line in handle.readlines():
            DEBUG and print(f"DEBUG>>> version peek scanner line {line=}")
            if cvrf_element_start in line or naive:
                naive.append(line.strip())
                DEBUG and print(f"DEBUG>>> version peek parser triggered {cvrf_element_start=}, {naive=}")
            if naive and any(cvrf_element_end in chunk for chunk in naive):
                DEBUG and print(f"DEBUG>>> version peek harvest done triggered {cvrf_element_end=}, {naive=}")
                break
            DEBUG and print(f"DEBUG>>> version peek normal harvest {naive=}")

    oasis_token = f'"http://docs.oasis-open.org/csaf/ns/csaf-cvrf/v{CRVF_DEFAULT_SEMANTIC_VERSION}/cvrf"'
    if any(oasis_token in chunk for chunk in naive):
        return CRVF_DEFAULT_SEMANTIC_VERSION
    pre_oasis_token = f'"http://www.icasi.org/CVRF/schema/cvrf/{CRVF_PRE_OASIS_SEMANTIC_VERSION}"'
    if any(pre_oasis_token in chunk for chunk in naive):
        return CRVF_PRE_OASIS_SEMANTIC_VERSION

    return None


def version_from(schema_path, document_path):
    """HACK A DID ACK derives non-default 1.1 version from path."""
    DEBUG and print(f"DEBUG>>> xml version derivation flat inspection {schema_path=}")
    if CRVF_PRE_OASIS_SEMANTIC_VERSION in str(schema_path):
        return CRVF_PRE_OASIS_SEMANTIC_VERSION
    if CRVF_DEFAULT_SEMANTIC_VERSION in str(schema_path):
        return CRVF_DEFAULT_SEMANTIC_VERSION
    DEBUG and print(f"DEBUG>>> xml version derivation deep call {document_path=}")
    return version_peek(document_path)


def validate(document, schema, conformance=None):
    """Validate the document against the schema."""
    if isinstance(document, dict):  # HACK A DID ACK
        conformance = conformance if conformance else jsonschema.draft7_format_checker
        DEBUG and print(f"DEBUG>>> caller site json validation {document=}, {schema=}, format_checker={conformance}")
        return jsonschema.validate(document, schema, format_checker=conformance)

    DEBUG and print(f"DEBUG>>> caller site xml loading {document=}, {schema=}, {conformance=}")
    xml_tree, message = load_xml(document)
    if not xml_tree:
        print(message)
        return 1
    request_version = version_from(schema, document)
    DEBUG and print(f"DEBUG>>> version detected {schema=}, {document=}, {request_version=}")
    found, version, ns = versions_xml(xml_tree, request_version)
    DEBUG and print(f"DEBUG>>> versions consistency {found=}, {version=}, {ns=}")
    catalog = CVRF_VERSION_CATALOG_MAP[request_version]
    DEBUG and print(f"DEBUG>>> caller site validation: {schema=}, {catalog=}, {xml_tree=}, {request_version=}")
    status, message = xml_validate(schema, catalog, xml_tree, request_version)
    if not DEBUG and not status:
        print(message)
    DEBUG and print(f"DEBUG>>> validation xml results {status=}, {message=}")
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
    DEBUG and print(f"DEBUG>>> versions from namespace callee site {root=}")
    not_found = '', None
    if root is None:
        return not_found

    str_rep_root = str(root)
    DEBUG and print(f"DEBUG>>> versions from namespace callee site naive match {str_rep_root=} start")
    for version, ns in CVRF_VERSION_NS_MAP.items():
        DEBUG and print(f"DEBUG>>> versions from namespace callee site naive trial {str_rep_root=}, {version=}, {ns=}")
        if version in str_rep_root:
            DEBUG and print(f"DEBUG>>> versions from namespace callee site naive match {root=}, {version=}, {ns=}")
            return version, ns
        DEBUG and print(f"DEBUG>>> versions from namespace callee site naive miss {root=}, {version=}, {ns=}")

    return not_found


def versions_xml(xml_tree, request_version):
    """Versions from cvrf namespace in xml tree and request version."""
    sem_ver, doc_cvrf_version = derive_version_from_namespace(xml_tree.getroot())
    req_cvrf_version = f"http://docs.oasis-open.org/csaf/ns/csaf-cvrf/v{request_version}/cvrf"

    DEBUG and print(f"DEBUG>>> versions xml callee site {sem_ver=}, {doc_cvrf_version=}, {xml_tree=}")
    if doc_cvrf_version:
        return doc_cvrf_version == req_cvrf_version, doc_cvrf_version, req_cvrf_version

    return False, None, req_cvrf_version


def cvrf_validate(f, xml_tree):
    """
    Validates a CVRF document

    f: file object containing the schema
    xml_tree: the serialized CVRF ElementTree object
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


def push_catalog(catalog, request_version):
    """Isolate side effect interface to os env -> libxml2 <- lxml."""
    fallback_catalog = CVRF_DEFAULT_CATALOG
    if request_version != CRVF_DEFAULT_SEMANTIC_VERSION:
        fallback_catalog = CVRF_PRE_OASIS_CATALOG
    catalog = catalog if catalog else fallback_catalog

    # If the supplied file is not a valid catalog.xml or doesn't exist lxml will fall back to using remote validation
    os.environ["XML_CATALOG_FILES"] = str(catalog)

    return catalog


def derive_schema_path(catalog, request_version, schema):
    """Handle the implicit schema case by falling back on locally provided schema (matching the catalog)."""
    if schema:
        DEBUG and print(f"DEBUG>>> xml validate try reading schema {catalog=}, {schema=}, catalog env=({os.getenv('XML_CATALOG_FILES')})")
    else:
        DEBUG and print(f"DEBUG>>> xml validate try reading local implicit schema {catalog=}, {schema=}, catalog env=({os.getenv('XML_CATALOG_FILES')})")
        # try to use local schema file
        fallback_schema = CVRF_DEFAULT_SCHEMA_FILE
        if request_version != CRVF_DEFAULT_SEMANTIC_VERSION:
            fallback_schema = CVRF_PRE_OASIS_SCHEMA_FILE
        schema = fallback_schema
    return schema


def xml_validate(schema, catalog, xml_tree, request_version):
    """Validate xml tree against given xml schema of request version assisted by catalog."""
    DEBUG and print(f"DEBUG>>> xml validate parameters: {schema=}, {catalog=}, {xml_tree=}, {request_version=}")
    catalog = push_catalog(catalog, request_version)
    schema = derive_schema_path(catalog, request_version, schema)

    try:
        with open(schema, 'r') as handle:
            DEBUG and print(f"DEBUG>>> xml validate success reading schema {catalog=}, {schema=}, catalog env=({os.getenv('XML_CATALOG_FILES')})")
            code, result = cvrf_validate(handle, xml_tree)
    except IOError as err:
        return False, f"validation of {xml_tree} against {schema} not performed due to IO error: {err}"

    if code is False:
        return False, f"validation of {xml_tree} against {schema} failed with error: {result}"

    return True, f"validation of {xml_tree} against {schema} succeeded with result: {result}"


def dispatch_embedding(DEBUG, argv, embedded, num_args, pos_args):
    if embedded:
        DEBUG and print(f"DEBUG>>> embedded dispatch {embedded=}, {argv=}, {num_args=}, {pos_args=}")
        json_token, xml_token = '{', '<'
        is_json = any(arg and str(arg).startswith(json_token) for arg in pos_args)
        is_xml = not is_json and any(arg and str(arg).startswith(xml_token) for arg in pos_args)
    else:
        DEBUG and print(f"DEBUG>>> non-embedded dispatch {embedded=}, {argv=}, {num_args=}, {pos_args=}")
        json_token, xml_token = '.json', '.xml'
        is_json = any(arg and str(arg).endswith(json_token) for arg in pos_args)
        is_xml = not is_json and any(arg and str(arg).endswith(xml_token) for arg in pos_args)
    document_data, document, schema = '', '', ''
    if not (embedded or is_json or is_xml):
        DEBUG and print(f"DEBUG>>> streaming dispatch {embedded=}, {argv=}, {num_args=}, {pos_args=}, {is_json=}, {is_xml=}")
        document_data = read_stdin()
        json_token, xml_token = '{', '<'
        is_json = document_data.startswith(json_token)
        is_xml = not is_json and document_data.startswith(xml_token)
    return document, document_data, is_json, is_xml, schema


def main(argv=None, embedded=False, debug=False):
    """Drive the validator.
    This function acts as the command line interface backend.
    There is some duplication to support testability.
    TODO(sthagen) the dispatch has become Rococo - needs Bauhaus again.
    """
    global DEBUG
    if debug:
        DEBUG = True
    argv = argv if argv else sys.argv[1:]
    num_args = len(argv)
    DEBUG and print(f"DEBUG>>> guarded dispatch {embedded=}, {argv=}, {num_args=}")
    if num_args > 2:  # Unclear what the inputs beyond two may be
        print("Usage: csaf-lint [schema.json] document.json")
        print("   or: csaf-lint < document.json")
        return 2
    pos_args = tuple(argv[n] if n < num_args and argv[n] else None for n in range(3))

    document, document_data, is_json, is_xml, schema = dispatch_embedding(DEBUG, argv, embedded, num_args, pos_args)

    DEBUG and print(f"DEBUG>>> post dispatch {embedded=}, {argv=}, {num_args=}, {pos_args=}, {is_json=}, {is_xml=}")

    if is_json:
        if num_args == 2:  # Schema file path is first
            schema = json.loads(pos_args[0]) if embedded else load(pos_args[0])
            document = json.loads(pos_args[1]) if embedded else load(pos_args[1])
        else:
            schema = load(CSAF_2_0_SCHEMA_PATH)
            if num_args == 1:  # Assume schema implicit, argument given is document file path
                document = json.loads(pos_args[0]) if embedded else load(pos_args[0])
            else:
                document = json.loads(document_data)

        return 0 if validate(document, schema) is None else 1

    if embedded and not is_xml and not is_json:
        print("Usage: csaf-lint [schema.xsd] document.xml")
        print(" note: no embedding support for non xml/json data")
        return 2

    if embedded and is_xml:
        print("Usage: csaf-lint [schema.xsd] document.xml")
        print(" note: no embedding supported for xsd/xml")
        return 2

    if num_args and is_xml:
        if num_args == 2:  # Schema file path is first
            schema = pos_args[0]
            document = pos_args[1]
        else:
            if num_args == 1:  # Assume schema implicit, argument given is document file path
                document = pos_args[0]
            else:
                print("Usage: csaf-lint [schema.xsd] document.xml")
                print(" note: no embedding supported for xsd/xml")
                return 2
            schema = CVRF_VERSION_SCHEMA_MAP[version_from(None, document)]

    return 0 if validate(document, schema) is None else 1
