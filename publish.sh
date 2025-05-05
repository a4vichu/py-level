#!/bin/bash

# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build the package
python -m pip install --upgrade pip
python -m pip install --upgrade build twine
python -m build

# Upload to PyPI
echo "Do you want to upload to PyPI? (y/n)"
read answer

if [ "$answer" = "y" ]; then
    python -m twine upload dist/*
else
    echo "Skipping upload to PyPI"
fi 