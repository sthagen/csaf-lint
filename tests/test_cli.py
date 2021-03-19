# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import io
import pathlib

import jsonschema
import pytest  # type: ignore

import csaf_lint.cli as cli


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


def test_main_nok_int(capsys):
    with pytest.raises(TypeError):
        cli.main(42)
    out, err = capsys.readouterr()
    assert not out
    assert not err


def test_main_nok_three_args(capsys):
    sequence_of_ints = ['/1', '/2', '/3']
    assert cli.main(sequence_of_ints) == 2
    out, err = capsys.readouterr()
    for term in USAGE_ERROR_TOKENS:
        assert term in out
