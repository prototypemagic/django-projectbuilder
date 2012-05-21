#!/bin/bash
# Steve Phillips / elimisteve
# Started 2012.02.05
# Updated 2012.04.27

if [ -z $1 ]; then
    echo Usage: `basename $0` project_name
    exit 0
fi

PROJECT_NAME=$1

# New
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ] ; do SOURCE="$(readlink "$SOURCE")"; done
THIS_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

echo "Creating $PROJECT_NAME directory and sub-directories"
echo
mkdir $PROJECT_NAME
chmod 777 $PROJECT_NAME  # FIXME
# Code is checked out to here as per bare/hooks/post-receive
mkdir $PROJECT_NAME/${PROJECT_NAME}_site
chmod 777 $PROJECT_NAME/${PROJECT_NAME}_site  # FIXME
git init --bare $PROJECT_NAME/bare
# Delete default hooks
rm $PROJECT_NAME/bare/hooks/*

# FIXME Assuming makes an ass, out of _you_
# Assumes 'default' virtualenv exists
(source /usr/local/bin/virtualenvwrapper.sh && cpvirtualenv default $PROJECT_NAME)

# Put our custom hooks in place
cp $THIS_DIR/server-hooks/* $PROJECT_NAME/bare/hooks/
for file in $PROJECT_NAME/bare/hooks/*; do
    sed -i "s/PROJECT_NAME/$PROJECT_NAME/g" $file
done

echo -e "If you're on a server, run\n\n    sudo bash -c \"./apachebuilder.sh $PROJECT_NAME\"\n\nto create and install an Apache config file, as well as set up sites-enabled and sites-available.\n"
echo -e "On your local dev machine, run something like\n\n    python djangobuilder.py --path path/to/$PROJECT_NAME\n"
echo -e "then push to the (probably remote) $PROJECT_NAME/bare/ directory.  Tell your local machine where to push to with\n"
echo -e "    git remote add origin ubuntu@my-django-powerde-site.com:/home/ubuntu/django_projects/$PROJECT_NAME/bare/\n"
echo -e "Then you can run something like the familiar\n"
echo -e "    git push origin master\n"
echo "to automatically deploy to this server! Just make sure to have Apache + mod_wsgi + Postgres installed."
#echo "Run proto-new-virtualhost-subdomain.py to manually create a new Apache config file."
