#!/usr/bin/env python
# Steve Phillips / elimisteve
# 2011.11.24

import sys

def usage():
    this_script = sys.argv[0].split('/')[-1]
    print this_script, "[domain_name] [project_name]"
    print "e.g.,", this_script, "cazooz.com cazooz"

if len(sys.argv) < 3:
    usage()
    sys.exit(0)

new_host = '''<VirtualHost *:80>
ServerName %s
WSGIScriptAlias / /home/ubuntu/django_projects/%s/apache/django.wsgi
Alias /admin_media/ /usr/local/lib/python2.6/dist-packages/django/contrib/admin/media/
Alias /media/ /home/ubuntu/django_projects/%s/media/

<Directory /usr/local/lib/python2.6/dist-packages/django/contrib/admin/media>
Order allow,deny
Allow from all
</Directory>

<Directory /home/ubuntu/django_projects/%s/media>
Order allow,deny
Allow from all
</Directory>
</VirtualHost>

''' % (sys.argv[1], sys.argv[2], sys.argv[2], sys.argv[2])

print new_host
