set -ex

flake8 wisp
flake8 test

mypy wisp
mypy test

py.test test
