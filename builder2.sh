#!/bin/bash
# Steve Phillips / elimisteve
# 2012.01.28

export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh 

export PROJECT_PATH=$1

echo "Creating new virtualenv for `basename $PROJECT_PATH`"
mkvirtualenv `basename $PROJECT_PATH` --no-site-packages
