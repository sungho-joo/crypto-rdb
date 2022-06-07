[![Python 3.9.7](https://img.shields.io/badge/python-3.9.7-blue.svg)](https://www.python.org/downloads/release/python-397/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/imports-isort-white)](https://pycqa.github.io/isort/)
[![Linting: flake8 & mypy & pylint](https://img.shields.io/badge/linting-flake8%20%26%20mypy%20%26%20pylint-green)](https://pypi.org/project/pytest-pylint/)

# Crypto RDB

**Crypto RDB** store web-scraped data from cryptocurrency exchanges API (e.g. [upbit](https://docs.upbit.com/)) into RDB (e.g. MariaDB) and supports basic visualization.

## Requirements

This repository is implemented and verified on **Python 3.9.7**.

## Installation

Clone this repository and run the following command.

### For Users
```bash
$ make init
```

### For Developers
```bash
$ make init-dev
```

## Usages

The high-level structure of the repository is:

    └── src
        ├── common
        ├── db
        ├── stat
        ├── websocket

TBD

### Development

We have setup automatic formatters and linters for this repository.

To run the formatters:

```bash
$ make format
```

To run the linters:

```bash
# Enable cache
$ make lint

# Disable cache
$ make lint-all
```

There are also unit tests in the repository.

```bash
$ make utest
```

New code should pass the formatters, linters, and unit tests before being submitted as a PR.
