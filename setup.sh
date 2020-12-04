#!/usr/bin/env bash
set euo -pipefail
# Run this script to set up your development environment.
# Works on Ubuntu 20.04.

# Install poetry dependency manager
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# Install dependencies
poetry install

# Download NLP model
poetry run python -m spacy download en_core_web_sm

# Test that the main program works
poetry run ./doc-import.py --help

echo "You’re ready to develop!"
