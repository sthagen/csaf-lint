# CSAF Lint

Experimental CSAF envelope and body profile validator.

[![license](badges/license-spdx-mit.svg)](https://git.sr.ht/~sthagen/csaf-lint/tree/default/item/LICENSE)
[![Country of Origin](badges/country-of-origin-name-switzerland-neutral.svg)](https://git.sr.ht/~sthagen/csaf-lint/tree/default/item/COUNTRY-OF-ORIGIN)
[![Export Classification Control Number (ECCN)](badges/export-control-classification-number_eccn-ear99-neutral.svg)](https://git.sr.ht/~sthagen/csaf-lint/tree/default/item/EXPORT-CONTROL-CLASSIFICATION-NUMBER)
[![Configuration](badges/configuration-sbom.svg)](third-party/index.html)

[![Version](badges/latest-release.svg)](https://pypi.python.org/pypi/csaf-lint/)
[![Downloads](badges/downloads-per-month.svg)](https://pepy.tech/project/csaf-lint)
[![Python](badges/python-versions.svg)](https://pypi.python.org/pypi/csaf-lint/)
[![Maintenance Status](badges/commits-per-year.svg)](https://git.sr.ht/~sthagen/csaf-lint/log)

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
The preferred public clone of `csaf-lint` is:

* [at sourcehut](https://git.sr.ht/~sthagen/csaf-lint) - a collection of tools useful for software development.

## Contributions

Please do not submit "pull requests" (I found no way to disable that "feature" on GitHub).
If you like to share small changes under the repositories license please kindly do so by sending a patchset.
You can either send such a patchset per email using [git send-email](https://git-send-email.io) or 
if you are a sourcehut user by selecting "Prepare a patchset" on the summary page of your fork at [sourcehut](https://git.sr.ht/).

## Support

Please kindly submit issues at <https://todo.sr.ht/~sthagen/csaf-lint> or write plain text email to <~sthagen/csaf-lint@lists.sr.ht> to submit patches and request support. Thanks.
