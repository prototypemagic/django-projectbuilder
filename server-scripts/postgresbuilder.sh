#!/bin/bash
# Steve Phillips / elimisteve
# Started 2012.05.21
# Finished v1 2012.08.06

# Modified version of script from
# http://lukeplant.me.uk/blog/posts/starter-fabfile-and-scripts-for-a-django-project-on-webfaction/

if [ $# -lt 2 ]; then
    echo "Usage: `basename $0` project_name DATABASES_PASSWORD_from_settings.py"
    exit 1
fi

project_name=$1
password=$2

db_name=$project_name
# NOTE: $username definition assumes settings.py-needed still defined
# 'USER' as  %(PROJECT_NAME)s_user
username=${project_name}_user

sudo -u postgres psql -a -U postgres -d template1 -c "CREATE USER $username WITH PASSWORD '$password';"
sudo -u postgres psql -a -U postgres -d template1 -c "CREATE DATABASE $db_name OWNER $username ENCODING 'UTF8';"
sudo -u postgres psql -a -U postgres -d template1 -c "GRANT ALL ON DATABASE $db_name TO $username;"
# Need create DB privileges to run tests.
sudo -u postgres psql -a -U postgres -d template1 -c "ALTER USER $username CREATEDB;"
