#!/bin/bash
# Steve Phillips / elimisteve
# 2012.02.05

if [ -z $1 ]; then
    echo Usage: `basename $0` project_name
    exit 0
fi

PROJECT_NAME=$1

echo "Creating $PROJECT_NAME directory and sub-directores"
mkdir $PROJECT_NAME
mkdir $PROJECT_NAME/${PROJECT_NAME}_site
git init --bare $PROJECT_NAME/bare
rm $PROJECT_NAME/bare/hooks/*

cp hooks/* $PROJECT_NAME/bare/hooks/
for file in $PROJECT_NAME/bare/hooks/*; do
    sed -i "s/PROJECT_NAME/$PROJECT_NAME/g" $file
done

echo "Now run proto-new-virtualhost-subdomain.py to create a new Apache config file"
