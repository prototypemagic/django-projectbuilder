#!/bin/bash
# Steve Phillips / elimisteve
# 2012.02.05

if [ -z $1 ]; then
    echo Usage: `basename $0` project_name
    exit 0
fi

PROJECT_NAME=$1

echo "Creating $PROJECT_NAME directory and sub-directories"
echo
mkdir $PROJECT_NAME
# Code is checked out to here as per bare/hooks/post-receive
mkdir $PROJECT_NAME/${PROJECT_NAME}_site
git init --bare $PROJECT_NAME/bare
# Delete default hooks
rm $PROJECT_NAME/bare/hooks/*

# Put our custom hooks in place
cp hooks/* $PROJECT_NAME/bare/hooks/
for file in $PROJECT_NAME/bare/hooks/*; do
    sed -i "s/PROJECT_NAME/$PROJECT_NAME/g" $file
done

echo "If you're on a server, run 'sudo apachebuilder.sh $PROJECT_NAME' to create and install an Apache config file, as well as set up sites-enabled and sites-available."
echo
echo "On your local dev machine, run 'python djangobuilder.py $PROJECT_NAME', then push to (the probably remote) $PROJECT_NAME/bare/ directory"
#echo "Run proto-new-virtualhost-subdomain.py to manually create a new Apache config file."
