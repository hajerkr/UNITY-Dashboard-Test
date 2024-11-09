#!/usr/bin/env bash
# upgrade pip first
python -m pip install --upgrade pip

# install wheel and setuptools first
pip install --upgrade wheel setuptools

# install numpy first as it's required by scipy
pip install numpy>=1.26.0

# install scipy
pip install scipy>=1.12.0

# then install remaining requirements
pip install -r requirements.txt