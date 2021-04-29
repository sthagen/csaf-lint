# -*- coding: utf-8 -*-
# pylint: disable=c-extension-no-member,expression-not-assigned,line-too-long,logging-fstring-interpolation
"""Visit CSAF/CVRF files and validate them against envelope (core) and given body profiles."""
import json
import logging
import os
import pathlib
import sys
import typing

import jsonschema  # type: ignore
from lxml import etree  # type: ignore


ENCODING = "utf-8"

APP = 'csaf-lint'

LOG = logging.getLogger()  # Temporary refactoring: module level logger
LOG_FOLDER = pathlib.Path('logs')
LOG_FILE = f'{APP}.log'
LOG_PATH = pathlib.Path(LOG_FOLDER, LOG_FILE) if LOG_FOLDER.is_dir() else pathlib.Path(LOG_FILE)
LOG_LEVEL = logging.INFO

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
DEBUG = bool(os.getenv(DEBUG_VAR))


def read_stdin():
    """Create document from stdin data."""
    LOG.debug("call site loading from stdin")
    return sys.stdin.read()


def load(file_path):
    """Create JSON object from file."""
    LOG.debug("call site file loading file_path=%s", file_path)
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
    LOG.debug("version peek cheap detect on path string document_path=%s", document_path)
    if CRVF_PRE_OASIS_SEMANTIC_VERSION in str(document_path):
        return CRVF_PRE_OASIS_SEMANTIC_VERSION
    if CRVF_DEFAULT_SEMANTIC_VERSION in str(document_path):
        return CRVF_DEFAULT_SEMANTIC_VERSION

    LOG.debug("version peek naive but deep detect on path content document_path=%s", document_path)
    cvrf_element_start = '<cvrf'
    cvrf_element_end = '>'
    naive = []
    with open(document_path) as handle:
        for line in handle.readlines():
            LOG.debug("version peek scanner line=%s", line)
            if cvrf_element_start in line or naive:
                naive.append(line.strip())
                LOG.debug("version peek parser triggered cvrf_element_start=%s, naive=%s", cvrf_element_start, naive)
            if naive and any(cvrf_element_end in chunk for chunk in naive):
                LOG.debug("version peek harvest done triggered cvrf_element_end=%s, naive=%s", cvrf_element_end, naive)
                break
            LOG.debug("version peek normal harvest naive=%s", naive)

    oasis_token = f'"http://docs.oasis-open.org/csaf/ns/csaf-cvrf/v{CRVF_DEFAULT_SEMANTIC_VERSION}/cvrf"'
    if any(oasis_token in chunk for chunk in naive):
        return CRVF_DEFAULT_SEMANTIC_VERSION
    pre_oasis_token = f'"http://www.icasi.org/CVRF/schema/cvrf/{CRVF_PRE_OASIS_SEMANTIC_VERSION}"'
    if any(pre_oasis_token in chunk for chunk in naive):
        return CRVF_PRE_OASIS_SEMANTIC_VERSION

    LOG.debug("version peek finally failed")
    return None


def version_from(schema_path, document_path):
    """HACK A DID ACK derives non-default 1.1 version from path."""
    LOG.debug("xml version derivation flat inspection schema_path=%s", schema_path)
    if CRVF_PRE_OASIS_SEMANTIC_VERSION in str(schema_path):
        return CRVF_PRE_OASIS_SEMANTIC_VERSION
    if CRVF_DEFAULT_SEMANTIC_VERSION in str(schema_path):
        return CRVF_DEFAULT_SEMANTIC_VERSION
    LOG.debug("xml version derivation deep call document_path=%s", document_path)
    return version_peek(document_path)


def validate_json(document, schema, conformance=None) -> typing.Tuple[int, str]:
    """Validate the JSON document against the schema."""
    conformance = conformance if conformance else jsonschema.draft7_format_checker
    LOG.debug(f"caller site json validation list(document.keys())={list(document.keys())},"
              f" list(schema.keys())={list(schema.keys())}, format_checker={conformance}")
    code, message = 0, "OK"
    try:
        jsonschema.validate(document, schema, format_checker=conformance)
    except jsonschema.exceptions.ValidationError as err:
        LOG.error(f"err.message={err.message} [err.validator={err.validator}] err.relative_path={err.relative_path}")
        code, message = 1, f"{err}"
    except jsonschema.exceptions.SchemaError as err:
        LOG.error(f"err.message={err.message} [err.validator={err.validator}] err.relative_path={err.relative_path}")
        code, message = 2, f"{err}"

    LOG.debug(f"success in JSON validation: code={code}, message={message}")
    return code, message


def validate(document, schema, conformance=None) -> typing.Tuple[int, str]:
    """Validate the document against the schema."""
    if isinstance(document, dict):  # HACK A DID ACK
        return validate_json(document, schema, conformance)

    LOG.debug(f"caller site xml loading document={document}, schema={schema}, conformance={conformance}")
    xml_tree, message = load_xml(document)
    if not xml_tree:
        LOG.error(message)
        return 1, "ERROR"
    request_version = version_from(schema, document)
    LOG.debug(f"version detected schema={schema}, document={document}, request_version={request_version}")
    found, version, namespace = versions_xml(xml_tree, request_version)
    LOG.debug(f"versions consistency found={found}, version={version}, namespace={namespace}")
    catalog = CVRF_VERSION_CATALOG_MAP[request_version]
    LOG.debug(f"caller site validation: schema={schema}, catalog={catalog}, xml_tree={xml_tree}, request_version={request_version}")
    status, message = xml_validate(schema, catalog, xml_tree, request_version)
    LOG.debug(f"validation xml results status={status}, message={message}")
    if status:
        return 0, "OK"
    LOG.warning(message)
    return 1, "ERROR"


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
    LOG.debug("versions from namespace callee site root=%s", root)
    not_found = '', None
    if root is None:
        return not_found

    str_rep_root = str(root)
    LOG.debug(f"versions from namespace callee site naive match str_rep_root={str_rep_root} start")
    for version, namespace in CVRF_VERSION_NS_MAP.items():
        LOG.debug(f"versions from namespace callee site naive trial str_rep_root={str_rep_root},"
                  f" version={version}, namespace={namespace}")
        if version in str_rep_root:
            LOG.debug(f"versions from namespace callee site naive match root={root},"
                      f" version={version}, namespace={namespace}")
            return version, namespace
        LOG.debug(f"versions from namespace callee site naive miss root={root},"
                  f" version={version}, namespace={namespace}")

    return not_found


def versions_xml(xml_tree, request_version):
    """Versions from cvrf namespace in xml tree and request version."""
    sem_ver, doc_cvrf_version = derive_version_from_namespace(xml_tree.getroot())
    req_cvrf_version = f"http://docs.oasis-open.org/csaf/ns/csaf-cvrf/v{request_version}/cvrf"

    LOG.debug(f"versions xml callee site sem_ver={sem_ver}, doc_cvrf_version={doc_cvrf_version}, xml_tree={xml_tree}")
    if doc_cvrf_version:
        return doc_cvrf_version == req_cvrf_version, doc_cvrf_version, req_cvrf_version

    return False, None, req_cvrf_version


def cvrf_validate(handle: typing.IO, xml_tree: etree.ElementTree) -> typing.Tuple[bool, str]:
    """Validates a CVRF document."""
    try:
        xmlschema_doc = etree.parse(handle)
    except etree.XMLSyntaxError as err:
        return False, f'Parsing error, schema document "{handle.name}" is not well-formed: {err}'
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
        LOG.debug(f"xml validate try reading schema catalog={catalog},"
                  f" schema={schema}, catalog env=({os.getenv('XML_CATALOG_FILES')})")
    else:
        LOG.debug(f"xml validate try reading local implicit schema catalog={catalog},"
                  f" schema={schema}, catalog env=({os.getenv('XML_CATALOG_FILES')})")
        # try to use local schema file
        fallback_schema = CVRF_DEFAULT_SCHEMA_FILE
        if request_version != CRVF_DEFAULT_SEMANTIC_VERSION:
            fallback_schema = CVRF_PRE_OASIS_SCHEMA_FILE
        schema = fallback_schema
    return schema


def xml_validate(schema, catalog, xml_tree, request_version):
    """Validate xml tree against given xml schema of request version assisted by catalog."""
    LOG.debug(f"xml validate parameters: schema={schema}, catalog={catalog},"
              f" xml_tree={xml_tree}, request_version={request_version}")
    catalog = push_catalog(catalog, request_version)
    schema = derive_schema_path(catalog, request_version, schema)

    try:
        with open(schema, 'r') as handle:
            LOG.debug(f"xml validate success reading schema catalog={catalog},"
                      f" schema={schema}, catalog env=({os.getenv('XML_CATALOG_FILES')})")
            code, result = cvrf_validate(handle, xml_tree)
    except IOError as err:
        return False, f"validation of {xml_tree} against {schema} not performed due to IO error: {err}"

    if code is False:
        return False, f"validation of {xml_tree} against {schema} failed with error: {result}"

    return True, f"validation of {xml_tree} against {schema} succeeded with result: {result}"


def dispatch_embedding(argv, embedded, num_args, pos_args):
    """Dispatch of embedded inputs (documents as arguments)."""
    if embedded:
        LOG.debug(f"embedded dispatch embedded={embedded}, argv={argv}, num_args={num_args}, pos_args={pos_args}")
        json_token, xml_token = '{', '<'
        is_json = any(arg and str(arg).startswith(json_token) for arg in pos_args)
        is_xml = not is_json and any(arg and str(arg).startswith(xml_token) for arg in pos_args)
    else:
        LOG.debug(f"non-embedded dispatch embedded={embedded}, argv={argv}, num_args={num_args}, pos_args={pos_args}")
        json_token, xml_token = '.json', '.xml'
        is_json = any(arg and str(arg).endswith(json_token) for arg in pos_args)
        is_xml = not is_json and any(arg and str(arg).endswith(xml_token) for arg in pos_args)
    document_data, document, schema = '', '', ''
    if not (embedded or is_json or is_xml):
        LOG.debug(f"streaming dispatch embedded={embedded}, argv={argv}, num_args={num_args}, pos_args={pos_args},"
                  f" is_json={is_json}, is_xml={is_xml}")
        document_data = read_stdin()
        json_token, xml_token = '{', '<'
        is_json = document_data.startswith(json_token)
        is_xml = not is_json and document_data.startswith(xml_token)
    return document, document_data, is_json, is_xml, schema


def init_logger(name=None, level=None):
    """Temporary refactoring: Initialize module level logger"""
    global LOG  # pylint: disable=global-statement

    log_format = {
        'format': '%(asctime)s %(levelname)s [%(name)s]: %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S',
        # 'filename': LOG_PATH,
        'level': LOG_LEVEL if level is None else level
    }
    logging.basicConfig(**log_format)
    LOG = logging.getLogger(APP if name is None else name)


def inputs_xml(num_args, pos_args):
    """Derive document and schema inputs for JSON format tasks."""
    if num_args == 2:  # Schema file path is first
        schema = pos_args[0]
        document = pos_args[1]
    else:
        if num_args == 1:  # Assume schema implicit, argument given is document file path
            document = pos_args[0]
            schema = CVRF_VERSION_SCHEMA_MAP[version_from(None, document)]
        else:
            document, schema = None, None

    return document, schema


def inputs_json(document_data, embedded, num_args, pos_args):
    """Derive document and schema inputs for JSON format tasks."""
    if num_args == 2:  # Schema file path is first
        schema = json.loads(pos_args[0]) if embedded else load(pos_args[0])
        document = json.loads(pos_args[1]) if embedded else load(pos_args[1])
    else:
        schema = load(CSAF_2_0_SCHEMA_PATH)
        if num_args == 1:  # Assume schema implicit, argument given is document file path
            document = json.loads(pos_args[0]) if embedded else load(pos_args[0])
        else:
            document = json.loads(document_data)

    return document, schema


def main(argv=None, embedded=False, debug=None):
    """Drive the validator.
    This function acts as the command line interface backend.
    There is some duplication to support testability.
    TODO(sthagen) the dispatch has become Rococo - needs Bauhaus again.
    """
    debug = DEBUG if debug is None else debug is True  # debug is None and DEBUG or debug is True
    init_logger(level=logging.DEBUG if debug else None)
    argv = argv if argv else sys.argv[1:]
    num_args = len(argv)
    LOG.debug(f"guarded dispatch embedded={embedded}, argv={argv}, num_args={num_args}")
    if num_args > 2:  # Unclear what the inputs beyond two may be
        LOG.error("Usage error (num_args > 2)")
        print("Usage: csaf-lint [schema.json] document.json")
        print("   or: csaf-lint < document.json")
        return 2
    pos_args = tuple(argv[n] if n < num_args and argv[n] else None for n in range(3))

    document, document_data, is_json, is_xml, schema = dispatch_embedding(argv, embedded, num_args, pos_args)

    LOG.debug(f"post dispatch embedded={embedded}, argv={argv}, num_args={num_args}, pos_args={pos_args},"
              f" is_json={is_json}, is_xml={is_xml}")

    if is_json:
        document, schema = inputs_json(document_data, embedded, num_args, pos_args)

        code, message = validate(document, schema)
        LOG.info(f"Validation(JSON): code={code}, message={message}")
        return code

    if embedded and not is_xml and not is_json:
        LOG.error("Usage error (embedded and not is_xml and not is_json)")
        print("Usage: csaf-lint [schema.xsd] document.xml")
        print(" note: no embedding support for non xml/json data")
        return 2

    if embedded and is_xml:
        LOG.error("Usage error (embedded and is_xml)")
        print("Usage: csaf-lint [schema.xsd] document.xml")
        print(" note: no embedding supported for xsd/xml")
        return 2

    if num_args and is_xml:
        document, schema = inputs_xml(num_args, pos_args)
    if document is None:
        LOG.error("Usage error (no embedding supported for xsd/xml)")
        print("Usage: csaf-lint [schema.xsd] document.xml")
        print(" note: no embedding supported for xsd/xml")
        return 2

    code, message = validate(document, schema)
    LOG.info(f"Validation(XML): code={code}, message={message}")
    return code
