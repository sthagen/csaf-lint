# CSAF Lint

Experimental CSAF envelope and body profile validator.

[License: MIT](https://github.com/sthagen/csaf-lint/blob/default/LICENSE)

Third party dependencies are documented in the folder [third-party](third-party/README.md).

[![version](https://img.shields.io/pypi/v/csaf-lint.svg?style=flat)](https://pypi.python.org/pypi/csaf-lint/)
[![downloads](https://pepy.tech/badge/csaf-lint/month)](https://pepy.tech/project/csaf-lint)
[![wheel](https://img.shields.io/pypi/wheel/csaf-lint.svg?style=flat)](https://pypi.python.org/pypi/csaf-lint/)
[![supported-versions](https://img.shields.io/pypi/pyversions/csaf-lint.svg?style=flat)](https://pypi.python.org/pypi/csaf-lint/)
[![supported-implementations](https://img.shields.io/pypi/implementation/csaf-lint.svg?style=flat)](https://pypi.python.org/pypi/csaf-lint/)

In short: The current version of the `csaf-lint` validates documents in various
Common Security Advisory Framework (CSAF) formats against built-in
or user custom schema files.

The supported  versions are:

* CSAF 2.0 (default is now the 2021.03.23 editor version)
* CSAF 1.2 (aka CVRF 1.2)
* CSAF 1.1 (aka CVRF 1.1)

## Caveat Emptor

1. Expect changes to the CSAF v2.0 support because the underlying OASIS specification
is undergoing development by the members of the OASIS technical committee.
   This may lead to breaking changes until the standard is published on
committee specification level.
   The current supported draft JSON Schema versions are from 2021-03-23, 2021-03-19, and 2021-03-07.
2. The previous versions namely CVRF 1.1 and 1.2 were in XML format.
3. The current version CSAF 2.0-candidates are in JSON Schema format.

Available on [PyPI as csaf-lint](https://pypi.org/project/csaf-lint/)

## Installing

Recommended installation of current experimental package:

```console
❯ python -m pipx install csaf-lint
```

## Bug Tracker

Any feature requests or bug reports shall go to the [todos of csaf-lint](https://todo.sr.ht/~sthagen/csaf-lint).

## Primary Source repository

The main source of `csaf-lint` is on a mountain in central Switzerland.
We use distributed version control (git).
There is no central hub.
Every clone can become a new source for the benefit of all.
The preferred public clones of `csaf-lint` are:

* [on codeberg](https://codeberg.org/sthagen/csaf-lint) - a democratic community-driven, non-profit software development platform operated by Codeberg e.V.
* [at sourcehut](https://git.sr.ht/~sthagen/csaf-lint) - a collection of tools useful for software development.

## Contributions

Please do not submit "pull requests" (I found no way to disable that "feature" on GitHub).
If you like to share small changes under the repositories license please kindly do so by sending a patchset.
You can either send such a patchset per email using [git send-email](https://git-send-email.io) or 
if you are a sourcehut user by selecting "Prepare a patchset" on the summary page of your fork at [sourcehut](https://git.sr.ht/).
