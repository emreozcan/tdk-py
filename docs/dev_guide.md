# Development Guide

Make sure you have [poetry](https://python-poetry.org/) installed.
To set up the development environment, run the following command to install
the project's dependencies.

:::{tab} with development and documentation tools
```bash
# in the shell
poetry install --with dev,docs
```
:::
:::{tab} only development tools
```bash
# in the shell
poetry install --with dev
```
:::

:::{tip}
The `--with dev` flag installs the development dependencies,
which includes
the pytest test runner,
mypy static type checker,
and the black code formatter.
:::

:::{tip}
The `--with docs` flag installs the documentation dependencies,
which includes
the Sphinx documentation generator
and extensions and themes for it.
:::

### Running the tests

```bash
# in the shell
poetry run pytest
```

### Running the static type checker

```bash
# in the shell
poetry run mypy src
```

### Formatting the code

```bash
# in the shell
poetry run black src
```

## Building the documentation

To build the documentation, the project's `docs` dependency group must be
installed.

```bash
# in the shell
poetry install --with docs
```

```bash
# in the shell
poetry run sphinx-autobuild docs docs/_build/html --watch src
```
