#!/usr/bin/env bash
pip install -r requirements.txt
sphinx-apidoc -M -o source/packages .. /*/migrations/* -H "Packages and Modules"

# Run this with your user/group if on linux
# chown -R 1001:1001 .
