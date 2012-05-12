#!/bin/bash
# Steve Phillips / elimisteve
# 2011.11.24

if [ $# -lt 2 ]; then
    echo "`basename $0` project_name project_password"
    exit 0
fi

project_name=$1
project_pass=$2

source /usr/local/bin/virtualenvwrapper.sh

cd /home/ubuntu/django_projects/$project_name
cp settings.py settings.py-orig
sed "s/PROJECT_NAME/$project_name/g" /home/ubuntu/proto/settings.py-general > settings.py
sed -i "s/PROJECT_PASS/$project_pass/g" settings.py

# Create directories stated in settings.py
mkdir /home/ubuntu/django_projects/$project_name/media
mkdir /home/ubuntu/django_projects/$project_name/templates
mkdir /home/ubuntu/django_projects/$project_name/apache

# Create virtualenv and install packages to it
mkvirtualenv $project_name --no-site-packages
#workon $project_name
#pip install -r /home/ubuntu/proto/requirements.txt -E $project_name
pip install Django Fabric South amqplib anyjson celery django-celery django-indexer django-paging django-picklefield django-sentry django-taggit django-templatetag-sugar eventlet greenlet ipython kombu lockfile paramiko psycopg2 pycrypto pyparsing python-daemon python-dateutil raven simplejson wsgiref yolk -E $project_name

# Generate SECRET_KEY and put it in settings.py
random_string=`python -c "import random, string; print ''.join([ random.choice(string.printable[:94]) for _ in range(50) ])"`
sed -i "s/RANDOM_STRING/$random_string/g" settings.py

# Configure Postgres
### Append username/DB name lines to /etc/postgresql/8.4/main/pg_hba.conf
### Use 'createuser' command to create new Postgres user

cp /home/ubuntu/proto/django.wsgi-general apache/django.wsgi
sed -i "s/PROJECT_NAME/$project_name/g" apache/django.wsgi
