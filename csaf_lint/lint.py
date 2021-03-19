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

ENCODING = "utf-8"

CSAF_2_0_SCHEMA_PATH = pathlib.Path('csaf_lint', 'schema', 'csaf', '2.0', 'csaf.json')

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


def validate(document, schema, conformance=None):
    """Validate the document against the schema."""
    conformance = conformance if conformance else jsonschema.draft7_format_checker
    return jsonschema.validate(document, schema, format_checker=conformance)


def main(argv=None, embedded=False):
    """Drive the validator."""
    argv = argv if argv else sys.argv[1:]
    if len(argv) > 2:  # Unclear what the inputs beyond two may be
        print("Usage: csaf-lint [schema.json] document.json")
        print("   or: csaf-lint < document.json")
        return 2

    if len(argv) == 2:  # Schema file path is first
        schema = json.loads(argv[0]) if embedded else load(argv[0])
        document = json.loads(argv[1]) if embedded else load(argv[1])
    else:
        schema = load(CSAF_2_0_SCHEMA_PATH)
        if len(argv) == 1:  # Assume schema implicit, argument given is document file path
            document = load(argv[0])
        else:
            document = read_stdin()

    return 0 if validate(document, schema) is None else 1
