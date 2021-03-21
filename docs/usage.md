# Usage Examples

## Installing

There are multiple ways to install / make available `csaf-lint`.

### Local Environment per pipx

A quite safe option to evaluate python packages is per `pipx`.

```bash
$ pipx install csaf-lint
```

Later upgrades can be installed per `pipx upgrade csaf-lint`

Assuming there is a valid CSAF v2.0 file inside in the current directory
with the name `valid_csaf_v_2_0.json` validation works like this:

```bash
$ csaf-lint valid_csaf_v_2_0.json
```
resulting in no output at all and a return code of `0` for success.

Another way to obtain the same result is to provide the document per standard input like:

```bash
$ csaf-lint < valid_csaf_v_2_0.json
```

### Install per `pip`

Another option to evaluate python packages on environment level is per `pip`.
It is good practice to trial pacakges at first inside a python virtual environment.

```bash
$ pip install csaf-lint
```

Later upgrades can be installed per `pip install --upgrade csaf-lint`

Assuming there is a valid CSAF v2.0 file inside in the current directory
with the name `valid_csaf_v_2_0.json` validation works like this
(note the underscore instead of the dash separating the words `csaf` and `lint`):

```bash
$ python -m csaf_lint valid_csaf_v_2_0.json
```
resulting in no output at all and a return code of `0` for success.

Another way to obtain the same result is to provide the document per standard input like:

```bash
$ python -m csaf_lint < valid_csaf_v_2_0.json
```
Also in this install mode (as with `pipx`) you can call the application `csaf-lint`.

### Install per `docker`

For now cf. [hub.docker.com as shagen/csaf-lint](https://hub.docker.com/r/shagen/csaf-lint)
to obtain insatll and initial usage instructions for the docker image.

### Inside Repository Clone

For contributing to `csaf-lint` development it is a good idea to fork
the repository and clone that fork to your work environment.

The following one-time install steps set up a working virtual environment
inside the clone directory (pyenv is used as example assuming the active python
interpreter is 3.9.2):
```bash
$ pyenv virtualenv fluffy-funicular-3-9-2
$ pyenv local fluffy-funicular-3-9-2
$ pip install --upgrade pip
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt
```

In case these steps succeed, inside this directory a complete development and
test environment should be ready to use.

#### Validating Documents

Executing the `csaf_lint` module (first two executions succeed, third fails):

```bash
$ python -m csaf_lint tests/fixtures/csaf-2.0/baseline/spam/01.json
$ python -m csaf_lint tests/fixtures/cvrf-no-version-given/is_wun_two.xml
$ python -m csaf_lint examples/empty_object.json 2>&1 | grep -i validat
    return 0 if validate(document, schema) is None else 1
  File ".../fluffy-funicular/csaf_lint/lint.py", line 145, in validate
    return jsonschema.validate(document, schema, format_checker=conformance)
  File ".../site-packages/jsonschema/validators.py", line 934, in validate
jsonschema.exceptions.ValidationError: 'document' is a required property
Failed validating 'required' in schema:
```

#### Executing the Tests

Executing the tests per `pytest`:

```bash
$ pytest
============================= test session starts =========================
platform ...
rootdir: ...fluffy-funicular, configfile: pyproject.toml
plugins: ...
collected 21 items

tests/test_cli.py .....                                              [ 23%]
tests/test_lint.py ................                                  [100%]

============================= 21 passed in 32.26s =========================
```
#### Executing Code Quality Analysis

Running `prospector`:

```bash
$ prospector
Check Information
=================
         Started: ...
        Finished: ...
      Time Taken: 2.32 seconds
       Formatter: grouped
        Profiles: default, no_doc_warnings, no_test_warnings, ...
      Strictness: None
  Libraries Used:
       Tools Run: dodgy, mccabe, pep8, profile-validator, pyflakes, pylint
  Messages Found: 0

```
