#!/bin/sh
# Kevin Xu / imkevinxu
# 2012.08.23

# Basic script to install all the dependencies for Django Project Builder
# Tested on a Mac OSX 10.7 Lion

# Installing pip, django, virtualenv, virtualenvwrapper
if [ -z `which pip` ]
    then
        echo "Installing pip..."
        sudo easy_install pip
fi

if [ -z `which django-admin.py` ]
    then
        echo "Installing django..."
        sudo pip install django
fi

if [ -z `which virtualenv` ]
    then
        echo "Installing virtualenv..."
        sudo pip install virtualenv
fi

if [ -z `which virtualenvwrapper.sh` ]
    then
        echo "Installing virtualenvwrapper..."
        sudo pip install virtualenvwrapper
fi

# Adds lines to the shell startup file so that virtualenvwrapper can work
# http://virtualenvwrapper.readthedocs.org/en/latest/install.html#shell-startup-file
if [ ! -d "$WORKON_HOME" ]
    then
        echo "Adding virtualenvwrapper variables to ~/.bash_profile"
        echo source `which virtualenvwrapper.sh` >> ~/.bash_profile
        source ~/.bash_profile
fi

# Fixes problem that occurs on OSX 10.7 Lion when making a new virtualenv,
# it goes looking for disutils but crashes if it can't find one
# http://stackoverflow.com/questions/3129852/python-cant-locate-distutils-path-on-mac-osx
sudo touch /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/distutils/__init__.py

# Detects if the user has git installed and prompts them to install it if not
if [ -z `which git` ]
    then
        echo "Detected git has not been installed"
        echo "INSTALL git here http://git-scm.com/downloads"
fi

echo "All dependencies installed!"