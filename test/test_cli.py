# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import io

import pytest  # type: ignore

import csaf_lint.cli as cli

CONTENT_FEATURES = ('document', 'document-product', 'document-vulnerability', 'full', 'spam')
USAGE_ERROR_EMBEDDING_TOKENS = ('ERROR:', 'embed', 'only', 'none', 'all')
USAGE_ERROR_TOKENS = ('Usage:', 'schema', 'document', 'or:')


def test_main_nok_more_than_two_int_args(capsys):
    with pytest.raises(TypeError):
        cli.main([1, 2, 3])


@pytest.mark.serial
def test_main_nok_read_embedded_json_object_from_argv(capsys):
    assert cli.main(['{}'], debug=False) == 1
    out, err = capsys.readouterr()
    assert not out
    assert not err


@pytest.mark.serial
def test_main_nok_read_empty_json_object_from_stdin(capsys, monkeypatch):
    monkeypatch.setattr('sys.stdin', io.StringIO('{}'))
    assert cli.main([], debug=False) == 2
    out, err = capsys.readouterr()
    assert out.startswith('Usage: csaf-lint [schema.json] document.json')
    assert not err


def test_main_nok_int(capsys):
    with pytest.raises(TypeError):
        cli.main(42)
    out, err = capsys.readouterr()
    assert not out
    assert not err


def test_main_nok_three_args(capsys):
    sequence_of_non_existing_paths = ['/1', '/2', '/3']
    message = r'2'
    with pytest.raises(SystemExit, match=message):
        cli.main(sequence_of_non_existing_paths)
    out, err = capsys.readouterr()
    for term in USAGE_ERROR_EMBEDDING_TOKENS:
        assert term in out
