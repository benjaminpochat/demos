#!/usr/bin/env bash
python3 -m coverage erase
python3 -m coverage run --source src/main -m unittest discover -s src -p *test*
python3 -m coverage html 
