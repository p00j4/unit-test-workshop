#!/bin/bash

set -x
owner=${1:-p00j4}
VENV_PATH=~/venv/test_env || true
if [ ! -d $VENV_PATH ]; then
	echo "Existing virtual env not found, creating new"
	mkdir -p $VENV_PATH
	cd $VENV_PATH
	virtualenv .
	git clone git@github.com:$owner/unit-test-workshop.git || true
fi
if [[ -z "$VENV_PATH" ]]; then
	echo "Activating virtual env"
	source ./bin/activate
fi
cd $VENV_PATH/unit-test-workshop
git checkout feature/test_cases || true
pwd
echo "************** PATH: "$VENV_PATH
#pip install -r requirements.txt
python setup.py install
python setup.py test
python `which nosetests` tests -s -vv  --with-xunit --with-xcover
ls -lrt
