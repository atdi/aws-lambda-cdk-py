#!/bin/bash

rm -rf build

mkdir -p "deploy/build/app"

#Copy the function
cp app/functions/app_api.py deploy/build/

## Package the code
cd build
python3.12 -m venv venv
source ./venv/bin/activate
pip install -r ../requirements_deployment.txt
deactivate
rm -rf venv/lib/python3.12/site-packages/pip*
rm -rf venv/lib/python3.12/site-packages/setuptools*
rm -rf venv/lib/python3.12/site-packages/distutils*
rm -rf venv/lib/python3.12/site-packages/pkg*
rm -rf venv/lib/python3.12/site-packages/_distutils_hack
rm -rf venv/lib/python3.12/site-packages/*dist-info
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
cp -r venv/lib/python3.12/site-packages/* .
rm -rf venv
zip -r lambda.zip .
