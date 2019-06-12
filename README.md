# Entity salience detection

[![Docker Build Status](https://img.shields.io/docker/cloud/build/kevin91nl/entity-salience.svg)](https://hub.docker.com/r/kevin91nl/entity-salience/)

This repository contains the code for my Master Thesis which is about salient entity detection in documents.

## Quick start

The following code loads data from the entity salience detection project:

```bash
docker run -it kevin91nl/entity-salience python -c "from dataset.loader import ExternalDataLoader; print(ExternalDataLoader().get('annotations').head(5))"
```

## Development

For development, there are several Docker containers. There exists a container for serving the notebooks, there exists a container for running tests and there exists a default container used for running the Python code. The different Docker containers are explained in this section.

## Git hooks installer

Make sure to install the Git hooks such that it checks whether the code adheres to a few standards (PEP-8 and Numpy docstrings) on each commit. The Git hooks are installed by executing the following command:

```bash
docker-compose up --build githook-installer
```

## Tests and checks

The test and checks are execute automatically by the pre-commit hook which is installed by the Git hooks installer. In order to run all tests and checks manually, execute the following command:

```bash
docker-compose up --build run-checks
```

## Notebook server

In order to serve the notebooks on `http://localhost:8888`, execute the following command:

```bash
docker-compose up --build lab
```