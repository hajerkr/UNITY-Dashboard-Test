#!/usr/bin/env bash
# upgrade pip first
python -m pip install --upgrade pip

# install wheel and setuptools first
pip install --upgrade wheel setuptools

# then install requirements
pip install -r requirements.txt