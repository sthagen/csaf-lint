#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
""""Visit folder tree with CSAF or CVRF documents, validate the latter, and generate reports."""
import os
import sys

import csaf_lint.lint as csaf_lint


# pylint: disable=expression-not-assigned
def main(argv=None):
    """Process the job."""
    argv = sys.argv[1:] if argv is None else argv
    return csaf_lint.main(argv)
