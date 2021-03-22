# CSAF Lint
Experimental CSAF envelope and body profile validator.

In short: The current version of the `csaf-lint` validates documents in various
Common Security Advisory Framework (CSAF) formats against built-in
or user custom schema files.

The supported  versions are:

* CSAF 2.0 (default is now the 2021.03.19 editor version)
* CSAF 1.2 (aka CVRF 1.2)
* CSAF 1.1 (aka CVRF 1.1)

## Caveat Emptor

1. Expect changes to the CSAF v2.0 support because the underlying OASIS specification
is undergoing development by the members of the OASIS technical committee.
   This may lead to breaking changes until the standard is published on
committee specification level.
   The current supported draft JSON Schema versions are from 2021-03-19 and 2021-03-07.
2. The previous versions namely CVRF 1.1 and 1.2 were in XML format.
3. The current version CSAF 2.0-candidates are in JSON Schema format.

Available on [PyPI as csaf-lint](https://pypi.org/project/csaf-lint/) and
[hub.docker.com as shagen/csaf-lint](https://hub.docker.com/r/shagen/csaf-lint)

## Status
Experimental.

## Random Statements

Cascaded shape schema validation via russian doll design? Maybe.

Practical validation should expose the most convenient structure for stacked profiles (always adding not subtracting).

Read the source, Lucy!
