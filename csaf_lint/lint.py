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

DEBUG_VAR = "CSL_DEBUG"
DEBUG = os.getenv(DEBUG_VAR)


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
    if len(argv) != 2:
        print("Validation requires two positional arguments: schema.json document.json")
        return 2

    schema = json.loads(argv[0]) if embedded else load(argv[0])
    document = json.loads(argv[1]) if embedded else load(argv[1])

    return 0 if validate(document, schema) is None else 1
