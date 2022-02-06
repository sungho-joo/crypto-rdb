# Crypto RDB

**Crypto RDB** store web-scraped data from cryptocurrency exchanges API (e.g. [upbit](https://docs.upbit.com/)) into RDB (e.g. MariaDB) and supports basic visualization.

## Requirements

This repository is implemented and verified on **Python 3.9.7**.

## Installation

Clone this repository and run the following command.

```shell
$ make setup
```

## Usages

The high-level structure of the repository is:

    ├── src
        ├── db
        ├── websocket
        └── utils
    └── configs

TBD

## Development

We have setup automatic formatters and linters for this repository.

To run the formatters:

```shell
$ make format
```

To run the linters:

```shell
$ make lint
```

New code should pass the formatters and the linters before being submitted as a PR.