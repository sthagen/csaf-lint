# Installing

There are multiple ways to install / make available `csaf-lint`.

### Local Environment per pipx

A quite safe option to evaluate python packages is per `pipx`.

```bash
$ pipx install csaf-lint
```

Later upgrades can be installed per `pipx upgrade csaf-lint`


### Install per `pip`

Another option to evaluate python packages on environment level is per `pip`.
It is good practice to trial pacakges at first inside a python virtual environment.

```bash
$ pip install csaf-lint
```

Later upgrades can be installed per `pip install --upgrade csaf-lint`

### Install per `docker`

For now cf. [hub.docker.com as shagen/csaf-lint](https://hub.docker.com/r/shagen/csaf-lint)
to obtain install and initial usage instructions for the docker image.

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
