# Entity salience detection

[![Docker Build Status](https://img.shields.io/docker/build/kevin91nl/entity-salience.svg)](https://hub.docker.com/r/kevin91nl/entity-salience/)

This repository contains the code for my Master Thesis which is about salient entity detection in documents.

## Development

## Git hooks

Make sure to install the Git hooks such that it checks whether the code adheres to a few standards on each commit. The Git hooks are installed by executing the following command:

`docker-compose up --build githook-installer`

## Run all checks

In order to run all checks manually, execute the following command:

`docker-compose up --build run-checks`