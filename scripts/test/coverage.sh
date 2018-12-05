#!/usr/bin/env bash
python3 -m coverage run --source src/main -m unittest discover -s src
python3 -m coverage html 
