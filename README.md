# Entity salience detection

[![Docker Build Status](https://img.shields.io/docker/cloud/build/kevin91nl/entity-salience.svg)](https://hub.docker.com/r/kevin91nl/entity-salience/)

This repository contains the code for my Master Thesis which is about salient entity detection in documents.

## Development

For development, there are several Docker containers. There exists a container for serving the notebooks, there exists a container for running tests and there exists a default container used for running the Python code. The different Docker containers are explained in this section.

## Git hooks

Make sure to install the Git hooks such that it checks whether the code adheres to a few standards (PEP-8 and Numpy docstrings) on each commit. The Git hooks are installed by executing the following command:

`docker-compose up --build githook-installer`

## Run all checks

In order to run all checks manually, execute the following command:

`docker-compose up --build run-checks`

## Notebooks

In order to serve the notebooks on `http://localhost:8888`, execute the following command:

`docker-compose up --build lab`