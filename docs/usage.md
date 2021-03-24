# Usage Examples

## Using the Service Script `csaf-lint`

Assuming there is a valid CSAF v2.0 file inside in the current directory
with the name `valid_csaf_v_2_0.json` validation works like this:

```bash
$ csaf-lint valid_csaf_v_2_0.json
2021-03-24 20:08:55 INFO [csaf-lint]: Validation(JSON): code=0, message='OK'
```
resulting in no output at all and a return code of `0` for success.

Another way to obtain the same result is to provide the document per standard input like:

```bash
$ csaf-lint < valid_csaf_v_2_0.json
2021-03-24 20:08:57 INFO [csaf-lint]: Validation(JSON): code=0, message='OK'
```

### Using the Python Module `csaf_lint`

Again, assuming there is a valid CSAF v2.0 file inside in the current directory
with the name `valid_csaf_v_2_0.json` validation works like this
(note the underscore instead of the dash separating the words `csaf` and `lint`):

```bash
$ python -m csaf_lint valid_csaf_v_2_0.json
2021-03-24 20:08:58 INFO [csaf-lint]: Validation(JSON): code=0, message='OK'
```
resulting in no output at all and a return code of `0` for success.

Another way to obtain the same result is to provide the document per standard input like:

```bash
$ python -m csaf_lint < valid_csaf_v_2_0.json
2021-03-24 20:08:59 INFO [csaf-lint]: Validation(JSON): code=0, message='OK'
```
Also in this install mode (as with `pipx`) you can call the application `csaf-lint`.

## Using the `docker` image `shagen/csaf-lint`

For now cf. [hub.docker.com as shagen/csaf-lint](https://hub.docker.com/r/shagen/csaf-lint)
to obtain insatll and initial usage instructions for the docker image.

## Inside a Repository Checkout

### Using the Module

Executing the `csaf_lint` module (first two executions succeed, third fails):

```bash
$ python -m csaf_lint tests/fixtures/csaf-2.0/baseline/spam/01.json
2021-03-24 19:20:50 INFO [csaf-lint]: Validation(JSON): code=0, message='OK'
$ python -m csaf_lint tests/fixtures/cvrf-no-version-given/is_wun_two.xml
2021-03-24 19:21:15 INFO [csaf-lint]: Validation(XML): code=0, message='OK'
$ python -m csaf_lint examples/empty_object.json 2>&1 | grep -i validat| head -1
2021-03-24 19:22:05 ERROR [csaf-lint]: err.message="'document' is a required property" [err.validator='required'] err.relative_path=deque([])
```
Switching between editor versions is supported by explicitly stating  
the path for the schema like for the 2021.03.19 editor version:
```bash
$ export SCHEMA="csaf_lint/schema/csaf/2021.03.19/csaf.json"
$ python -m csaf_lint $SCHEMA validate_me_as_csaf.json
2021-03-24 19:51:30 INFO [csaf-lint]: Validation(JSON): code=0, message='OK'
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

For intermediate local development feedback (exclude the slow tests and  
report in a terse manner) excluding the complete corpus tests:
```bash
$ PYTEST_ADDOPTS="-q -m 'not slow'" pytest
...................                                                  [100%]
19 passed, 2 deselected in 10.02s
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
Running `mypy`:

```bash
$ mypy csaf_lint
Success: no issues found in 4 source files
```
