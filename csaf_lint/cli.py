#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Visit folder tree with CSAF or CVRF documents, validate the latter, and generate reports."""
import pathlib
import os
import sys

import csaf_lint.lint as lint

DEBUG_VAR = "CSL_DEBUG"
DEBUG = bool(os.getenv(DEBUG_VAR))


# pylint: disable=expression-not-assigned
def main(argv=None, debug=None):
    """Dispatch processing of the job.
    This is the strings only command line interface.
    For python API use interact with lint functions directly.
    """
    argv = sys.argv[1:] if argv is None else argv
    embedded = False
    debug = debug if debug else DEBUG
    for arg in argv:
        if not pathlib.Path(arg).is_file():
            if not embedded:
                embedded = True
            else:
                print("ERROR: embedding only works for none or all.")
                sys.exit(2)

    return lint.main(argv, embedded=embedded, debug=debug)
