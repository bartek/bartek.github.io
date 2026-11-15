#!/bin/bash
set -e

# Match the Python version used in CI (.github/workflows/build.yml)
python3.13 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt
