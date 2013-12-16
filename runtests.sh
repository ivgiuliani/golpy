#!/bin/sh
env PYTHONPATH="." python -m unittest discover golpy/tests -p 'test_*.py'
