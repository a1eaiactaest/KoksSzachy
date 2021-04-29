#!/bin/bash -e

echo "Running tests"

if (pytest -q | grep failed &> /dev/null)
then
  echo -e "\nTests didn't pass, aborting"
  exit
fi

pytest
rm -rf dist build
python3 setup.py sdist bdist_wheel
twine upload dist/*
