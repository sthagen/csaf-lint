# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long
"""Visit CSAF/CVRF files and validate them against envelope (core) and given body profiles."""
import copy
import csv
import datetime as dti
import hashlib
import lzma
import os
import pathlib
import subprocess
import sys

DEBUG_VAR = "AG_DEBUG"
DEBUG = os.getenv(DEBUG_VAR)


def main(argv=None):
    """Drive the validator."""
    argv = argv if argv else sys.argv[1:]
    if not argv:
        print("ERROR arguments expected.", file=sys.stderr)
        return 2
