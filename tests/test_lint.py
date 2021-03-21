# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import pathlib

import jsonschema
import pytest  # type: ignore

import csaf_lint.lint as lint

CONTENT_FEATURES = ('document', 'document-product', 'document-vulnerability', 'full', 'spam')
USAGE_ERROR_TOKENS = ('requires', 'two', 'schema', 'document')


def test_main_validate_spam_default_ok(capsys):
    n = 1
    nn = f'{n:02d}'
    a_document_path = pathlib.Path('tests', 'fixtures', 'csaf-2.0', 'baseline', 'spam', f'{nn}.json')
    argv = [a_document_path]
    assert lint.main(argv=argv) == 0
    out, err = capsys.readouterr()
    assert not out
    assert not err


def test_main_validate_spam_ok(capsys):
    """
    python -m csaf_lint csaf_lint/schema/csaf/2.0/csaf.json tests/fixtures/csaf-2.0/baseline/spam/01.json
    returns 0 and no additional information
    """
    for n in range(1, 11):
        nn = f'{n:02d}'
        a_document_path = pathlib.Path('tests', 'fixtures', 'csaf-2.0', 'baseline', 'spam', f'{nn}.json')
        argv = [lint.CSAF_2_0_SCHEMA_PATH, a_document_path]
        assert lint.main(argv=argv) == 0
        out, err = capsys.readouterr()
        assert not out
        assert not err


def test_main_validate_spam_nok():
    """
    python -m csaf_lint csaf_lint/schema/csaf/2.0/csaf.json tests/fixtures/csaf-2.0/invalid/spam/01.json
    returns 1 and plenty of information
    """
    a_document_path = pathlib.Path('tests', 'fixtures', 'csaf-2.0', 'invalid', 'spam', '01.json')
    argv = [lint.CSAF_2_0_SCHEMA_PATH, a_document_path]
    message = r"'csaf_version' is a required property"
    with pytest.raises(jsonschema.exceptions.ValidationError, match=message):
        lint.main(argv=argv)


#@pytest.mark.skip(reason='slow')
def test_main_validate_rest_ok(capsys):
    for content in CONTENT_FEATURES[:-1]:
        for n in range(1, 11):
            nn = f'{n:02d}'
            a_document_path = pathlib.Path('tests', 'fixtures', 'csaf-2.0', 'baseline', content, f'{nn}.json')
            argv = [lint.CSAF_2_0_SCHEMA_PATH, a_document_path]
            try:
                assert lint.main(argv=argv) == 0
            except jsonschema.exceptions.ValidationError as err:
                raise ValueError(f"failed validation for {a_document_path} in {test_main_validate_rest_ok}. Details: {err}")
            out, err = capsys.readouterr()
            assert not out
            assert not err


#@pytest.mark.skip(reason='slow')
def test_main_validate_rest_nok():
    for content in CONTENT_FEATURES[:-1]:
        for n in range(1, 11):
            nn = f'{n:02d}'
            a_document_path = pathlib.Path('tests', 'fixtures', 'csaf-2.0', 'invalid', content, f'{nn}.json')
            argv = [lint.CSAF_2_0_SCHEMA_PATH, a_document_path]
            try:
                lint.main(argv=argv)
                raise ValueError(f"failed validation for {a_document_path} in {test_main_validate_rest_ok}.")
            except jsonschema.exceptions.ValidationError:
                pass


def test_main_nok_non_existing_folder_(capsys):
    nef = 'folder_does_not_exist'
    a_document_path = pathlib.Path(nef, 'no_doc.json')
    assert pathlib.Path(nef).is_dir() is False, f"Unexpected folder {nef} exists which breaks this test"
    message = r"\[Errno 2\] No such file or directory: '%s'" % (a_document_path,)
    with pytest.raises(FileNotFoundError, match=message):
        lint.main([lint.CSAF_2_0_SCHEMA_PATH, a_document_path])
    out, err = capsys.readouterr()
    assert not out
    assert not err


def test_main_validate_xml_cvrf_1_2_default_ok(capsys):
    a_schema_path = pathlib.Path('csaf_lint', 'schema', 'cvrf', '1.2', 'cvrf.xsd')
    a_document_path = pathlib.Path('tests', 'fixtures', 'cvrf-1.2', 'baseline', '01.xml')  # cvrf_1.2_example_a.xml
    argv = [str(a_schema_path), str(a_document_path)]
    assert lint.main(argv=argv, embedded=False, debug=False) == 0
    out, err = capsys.readouterr()
    assert not out
    assert not err
