#!/usr/bin/env python
# Steve Phillips / elimisteve
# 2012.01.28

#
# Requires fabric, virtualenv, and virtualenvwrapper
#

# FIXME This shouldn't be hard-coded
# FIXME Hardcode it for now!
GENERIC_SCRIPTS_PATH = ''

from fabric.api import local
#import pbs
import commands, pbs, os, random, string, sys

USAGE = '%s /path/to/new/project_name' % (sys.argv[0])
FUTURE_USAGE = USAGE + ' [--cms] [--zinnia]'

if len(sys.argv) < 2:
    print USAGE
    sys.exit(0)

# FIXME Every file in generic_scripts and *-generic should be listed
# here... or we can copy entire directories
pathify = {
    # 'urls_dev.py':       '',
    'django.wsgi':       'apache/',
    'model_forms.py':    '%(PROJECT_NAME)s/',
    'models.py':         '%(PROJECT_NAME)s/',
    'requirements.txt':  '',
    'settings.py':       '',
    'settings_local.py': '',
    'urls.py':           '',
    'views.py':          '%(PROJECT_NAME)s/%(PROJECT_NAME)s/',
    'views.py':          '%(PROJECT_NAME)s/',
}

HOME_DIR = os.path.expandvars('$HOME').rstrip('/') + '/'

# Trailing / may be included or excluded
PROJECT_PATH = sys.argv[1].rstrip('/') + '/'
BASE_PATH, PROJECT_NAME = [path[:-1], path[-1] for path in PROJECT_PATH.split('/')[:-1]]
BASE_PATH = '/'.join(BASE_PATH)

# Make virtualenv
# FIXME Shouldn't assume the location of virtualenvwrapper.sh
local('bash -c "source /usr/local/bin/virtualenvwrapper.sh && mkvirtualenv %s"' %
      (PROJECT_NAME))
      #(pbs.which('virtualenvwrapper.sh'), ))
##VIRTUALENV_PATH = HOME_DIR + '.virtualenvs/' + PROJECT_NAME

# Make directories
# FIXME Add more dirs to this list
for dir_name in ['', 'media', 'static', 'templates', 'apache']:
    os.mkdir(PROJECT_PATH + dir_name)

SECRET_KEY = ''.join([ random.choice(string.printable[:94].replace("'", "")) for _ in range(50) ])

replacement_values = {
    'PROJECT_NAME':     PROJECT_NAME,
    'PROJECT_PASSWORD': PROJECT_PASSWORD,
    'BASE_PATH':        BASE_PATH,
    'SECRET_KEY':       SECRET_KEY,
}

generic_files = [x for x in os.listdir(GENERIC_SCRIPTS_PATH)
                 if x.endswith('-generic')]

for filename in generic_files:
    # Grab *-generic filenames
    f_read = open(GENERIC_SCRIPTS_PATH + filename, 'r')
    contents = f.read()
    f.close()

    # Replace %(SECRET_KEY)s, etc with new value for new project
    new_filename = filename.replace('-generic', '')
    # Path names include '%(PROJECT_NAME)s', etc
    file_path = pathify[new_filename] % replacement_values
    f_write = open(PROJECT_PATH + , 'w')
    new_contents = contents % replacement_values
    f_write.write(new_contents)
    f_write.close()
