# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import io
import pathlib

import jsonschema
import pytest  # type: ignore

import csaf_lint.cli as cli

A_SCHEMA_PATH = pathlib.Path('csaf_lint', 'schema', 'csaf', '2.0', 'csaf.json')
CONTENT_FEATURES = ('document', 'document-product', 'document-vulnerability', 'full', 'spam')
USAGE_ERROR_TOKENS = ('Usage:', 'schema', 'document', 'or:')


def test_main_nok_more_than_two_args(capsys):
    assert cli.main([1, 2, 3]) == 2
    out, err = capsys.readouterr()
    for term in USAGE_ERROR_TOKENS:
        assert term in out


def test_main_nok_read_empty_json_object_from_stdin(monkeypatch):
    monkeypatch.setattr('sys.stdin', io.StringIO('{}'))
    message = r"'document' is a required property"
    with pytest.raises(jsonschema.exceptions.ValidationError, match=message):
        cli.main([])


def test_main_nok_int_(capsys):
    with pytest.raises(TypeError):
        cli.main(42)
    out, err = capsys.readouterr()
    assert not out
    assert not err


def test_main_nok_ints_(capsys):
    sequence_of_ints = [1, 2, 3]
    assert cli.main(sequence_of_ints) == 2
    out, err = capsys.readouterr()
    for term in USAGE_ERROR_TOKENS:
        assert term in out


def test_main_nok_non_existing_folder_(capsys):
    nef = non_existing_folder_path = 'folder_does_not_exist'
    a_document_path = pathlib.Path(nef, 'no_doc.json')
    assert pathlib.Path(nef).is_dir() is False, f"Unexpected folder {nef} exists which breaks this test"
    message = r"\[Errno 2\] No such file or directory: '%s'" % (a_document_path,)
    with pytest.raises(FileNotFoundError, match=message):
        cli.main([A_SCHEMA_PATH, a_document_path])
    out, err = capsys.readouterr()

