# -*- coding: utf-8 -*-
import os
import pathlib
from unittest import mock

import jsonschema
import pytest  # type: ignore
from lxml import etree  # type: ignore

import csaf_lint.lint as lint

CONTENT_FEATURES = ('document', 'document-product', 'document-vulnerability', 'full', 'spam')
USAGE_ERROR_TOKENS = ('requires', 'two', 'schema', 'document')
USAGE_ERROR_NO_EMBEDDING_UNKNOWN_TOKENS = ('no', 'embed', 'support', 'non')
USAGE_ERROR_NO_EMBEDDING_XML_TOKENS = ('no', 'embed', 'support', 'xml')
EMPTY_CATALOG_MAPPING = {'XML_CATALOG_FILES': ''}

CVRF_IMPLICIT_1_2_DOCUMENT_PATH = pathlib.Path(
    'test', 'fixtures', 'cvrf-no-version-given', 'is_wun_two.xml'
)  # cvrf_1.2_example_a.xml
CVRF_IMPLICIT_1_1_DOCUMENT_PATH = pathlib.Path(
    'test', 'fixtures', 'cvrf-no-version-given', 'is_wun_wun.xml'
)  # CVRF-1.1-cisco-sa-20110525-rvs4000.xml


def test_main_embedded_unknown_nok(capsys):
    assert lint.main(argv=['foo'], embedded=True, debug=False) == 2
    out, _ = capsys.readouterr()
    for token in USAGE_ERROR_NO_EMBEDDING_UNKNOWN_TOKENS:
        assert token in out

    assert lint.main(argv=['foo', 'bar'], embedded=True, debug=False) == 2
    out, _ = capsys.readouterr()
    for token in USAGE_ERROR_NO_EMBEDDING_UNKNOWN_TOKENS:
        assert token in out


def test_main_embedded_xml_nok(capsys):
    assert lint.main(argv=['<foo>'], embedded=True, debug=False) == 2
    out, _ = capsys.readouterr()
    for token in USAGE_ERROR_NO_EMBEDDING_XML_TOKENS:
        assert token in out

    assert lint.main(argv=['<foo>', '<bar>'], embedded=True, debug=False) == 2
    out, _ = capsys.readouterr()
    for token in USAGE_ERROR_NO_EMBEDDING_XML_TOKENS:
        assert token in out


def test_derive_version_from_namespace_nok():
    assert lint.derive_version_from_namespace(None) == ('', None)


def test_derive_schema_path_nok():
    assert lint.derive_schema_path(object(), '42', None) == lint.CVRF_PRE_OASIS_SCHEMA_FILE


def test_main_too_many_args_nok():
    assert lint.main(['a', 'b', 'c']) == 2


def test_inputs_xml_empty_nok():
    assert lint.inputs_xml(0, []) == (None, None)


def test_version_from_explicit_cvrf_1_x_in_schema_path():
    for indicator in (lint.CRVF_DEFAULT_SEMANTIC_VERSION, lint.CRVF_PRE_OASIS_SEMANTIC_VERSION):
        assert lint.version_from(schema_path=indicator, document_path=None) == indicator


def test_version_from_explicit_cvrf_1_x_in_document_path():
    for indicator in (lint.CRVF_DEFAULT_SEMANTIC_VERSION, lint.CRVF_PRE_OASIS_SEMANTIC_VERSION):
        assert lint.version_from(schema_path='', document_path=indicator) == indicator


def test_version_from_implicit_cvrf_1_x_in_document_path():
    version_document_map = {
        lint.CRVF_DEFAULT_SEMANTIC_VERSION: CVRF_IMPLICIT_1_2_DOCUMENT_PATH,
        lint.CRVF_PRE_OASIS_SEMANTIC_VERSION: CVRF_IMPLICIT_1_1_DOCUMENT_PATH,
    }
    for version, document_path in version_document_map.items():
        assert lint.version_from(schema_path='', document_path=document_path) == version


def test_main_validate_spam_default_ok(capsys):
    n = 1
    nn = f'{n:02d}'
    a_document_path = pathlib.Path('test', 'fixtures', 'csaf-2.0', 'baseline', 'spam', f'{nn}.json')
    argv = [a_document_path]
    assert lint.main(argv=argv, embedded=False, debug=False) == 0
    _, err = capsys.readouterr()
    assert not err


@pytest.mark.serial
def test_main_validate_spam_ok(capsys):
    """
    python -m csaf_lint csaf_lint/schema/csaf/2.0/csaf.json tests/fixtures/csaf-2.0/baseline/spam/01.json
    returns 0 and no additional information
    """
    for n in range(1, 11):
        nn = f'{n:02d}'
        a_document_path = pathlib.Path('test', 'fixtures', 'csaf-2.0', 'baseline', 'spam', f'{nn}.json')
        argv = [lint.CSAF_2_0_SCHEMA_PATH, a_document_path]
        assert lint.main(argv=argv, embedded=False, debug=False) == 0
        _, err = capsys.readouterr()
        assert not err


@pytest.mark.serial
def test_main_validate_spam_nok():
    a_document_path = pathlib.Path('test', 'fixtures', 'csaf-2.0', 'invalid', 'spam', '01.json')
    argv = [lint.CSAF_2_0_SCHEMA_PATH, a_document_path]
    assert lint.main(argv=argv, embedded=False, debug=False) == 1


@pytest.mark.serial
def test_main_nok_non_existing_folder_(capsys):
    nef = 'folder_does_not_exist'
    a_document_path = pathlib.Path(nef, 'no_doc.json')
    assert pathlib.Path(nef).is_dir() is False, f'Unexpected folder {nef} exists which breaks this test'
    message = r"\[Errno 2\] No such file or directory: '%s'" % (a_document_path,)
    with pytest.raises(FileNotFoundError, match=message):
        lint.main([lint.CSAF_2_0_SCHEMA_PATH, a_document_path], embedded=False, debug=False)
    _, err = capsys.readouterr()
    assert not err


@pytest.mark.serial
@mock.patch.dict(os.environ, EMPTY_CATALOG_MAPPING, clear=True)
def test_main_validate_xml_cvrf_1_2_schema_and_document_ok(capsys):
    a_schema_path = pathlib.Path('csaf_lint', 'schema', 'cvrf', '1.2', 'cvrf.xsd')
    a_document_path = pathlib.Path('test', 'fixtures', 'cvrf-1.2', 'baseline', '01.xml')  # cvrf_1.2_example_a.xml
    argv = [str(a_schema_path), str(a_document_path)]
    assert lint.main(argv=argv, embedded=False, debug=False) == 0
    _, err = capsys.readouterr()
    assert not err


@pytest.mark.serial
@mock.patch.dict(os.environ, EMPTY_CATALOG_MAPPING, clear=True)
def test_main_validate_xml_cvrf_1_2_document_only_version_in_path_ok(capsys):
    a_document_path = pathlib.Path('test', 'fixtures', 'cvrf-1.2', 'baseline', '01.xml')  # cvrf_1.2_example_a.xml
    argv = [str(a_document_path)]
    assert lint.main(argv=argv, embedded=False, debug=False) == 0
    _, err = capsys.readouterr()
    assert not err


@pytest.mark.serial
@mock.patch.dict(os.environ, EMPTY_CATALOG_MAPPING, clear=True)
def test_main_validate_xml_cvrf_1_2_document_only_version_not_in_path_ok():
    a_document_path = CVRF_IMPLICIT_1_2_DOCUMENT_PATH
    argv = [str(a_document_path)]
    assert lint.main(argv=argv, embedded=False, debug=False) == 0, 'OK'


@pytest.mark.serial
@mock.patch.dict(os.environ, EMPTY_CATALOG_MAPPING, clear=True)
def test_main_validate_xml_cvrf_1_1_document_only_version_not_in_path_ok(capsys):
    a_document_path = CVRF_IMPLICIT_1_1_DOCUMENT_PATH
    argv = [str(a_document_path)]
    try:
        assert lint.main(argv=argv, embedded=False, debug=False) == 0
    except etree.XMLSchemaParseError:
        assert os.getenv('XML_CATALOG_FILES', '') == 'csaf_lint/schema/catalog_1_1.xml'


@pytest.mark.serial
@mock.patch.dict(os.environ, EMPTY_CATALOG_MAPPING, clear=True)
def test_main_validate_xml_cvrf_1_1_document_only_version_in_path_ok(capsys):
    a_document_path = pathlib.Path(
        'test', 'fixtures', 'cvrf-1.1', 'baseline', '01.xml'
    )  # CVRF-1.1-cisco-sa-20110525-rvs4000.xml
    argv = [str(a_document_path)]
    try:
        assert lint.main(argv=argv, embedded=False, debug=False) == 0
    except etree.XMLSchemaParseError:
        assert os.getenv('XML_CATALOG_FILES', '') == 'csaf_lint/schema/catalog_1_1.xml'


@pytest.mark.serial
@pytest.mark.slow
def test_main_validate_rest_ok(capsys):
    for content in CONTENT_FEATURES[:-1]:
        for n in range(1, 11):
            nn = f'{n:02d}'
            a_document_path = pathlib.Path('test', 'fixtures', 'csaf-2.0', 'baseline', content, f'{nn}.json')
            argv = [lint.CSAF_2_0_SCHEMA_PATH, a_document_path]
            try:
                code = lint.main(argv=argv, embedded=False, debug=False)
                assert code in (0, 1)
            except jsonschema.exceptions.ValidationError as err:
                raise ValueError(
                    f'failed validation for {a_document_path} in {test_main_validate_rest_ok}. Details: {err}'
                )
            _, err = capsys.readouterr()
            assert not err


@pytest.mark.serial
@pytest.mark.slow
def test_main_validate_rest_nok():
    for content in CONTENT_FEATURES[:-1]:
        for n in range(1, 11):
            nn = f'{n:02d}'
            a_document_path = pathlib.Path('test', 'fixtures', 'csaf-2.0', 'invalid', content, f'{nn}.json')
            argv = [lint.CSAF_2_0_SCHEMA_PATH, a_document_path]
            assert lint.main(argv=argv, embedded=False, debug=False) == 1, 'ERROR'
