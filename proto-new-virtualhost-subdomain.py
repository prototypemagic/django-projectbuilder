#!/usr/bin/env python
# Steve Phillips / elimisteve
# 2011.11.24

import sys

def usage():
    this_script = sys.argv[0].split('/')[-1]
    print this_script, "project_name"
    print "e.g.,", this_script, "cazooz"

if len(sys.argv) < 2:
    usage()
    sys.exit(0)

new_host = '''<VirtualHost *:80>
ServerName %(PROJECT_NAME)s.prototypemagic.com
WSGIScriptAlias / /home/ubuntu/django_projects/%(PROJECT_NAME)s/%(PROJECT_NAME)s_site/apache/django.wsgi
Alias /admin_media/ /usr/local/lib/python2.6/dist-packages/django/contrib/admin/media/
Alias /media/ /home/ubuntu/django_projects/%(PROJECT_NAME)s/%(PROJECT_NAME)s_site/media/

<Directory /usr/local/lib/python2.6/dist-packages/django/contrib/admin/media>
Order allow,deny
Allow from all
</Directory>

<Directory /home/ubuntu/django_projects/%(PROJECT_NAME)s/%(PROJECT_NAME)s_site/media>
Order allow,deny
Allow from all
</Directory>
</VirtualHost>
''' % {'PROJECT_NAME': sys.argv[1]}

print new_host
