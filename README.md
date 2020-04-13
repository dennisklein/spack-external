# Spack extension `external`

Provides new subcommand-family `spack external *` to explore options on how to improve the situation with spack's basic external package support.

## Status

Experimental

## Prerequisites

Developed against this modified spack: https://github.com/dennisklein/spack/tree/spack-external-dev

## Installation

Add the following config to `~/.spack/config.yaml`:

```yaml
config:
  extensions:
  - /path/to/clone/of/this/repo
```

## Usage

```
$ spack external -h
usage: spack external [-h] SUBCOMMAND ...

manipulate external package config files

positional arguments:
  SUBCOMMAND
    status (st)
               show which external packages are used

optional arguments:
  -h, --help   show this help message and exit
```
