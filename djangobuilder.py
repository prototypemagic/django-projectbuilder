#!/usr/bin/env python
#
#   Authors:
#   Steve Phillips -- steve@builtbyptm.com
#   AJ v Bahnken   -- aj@builtbyptm.com

#
# Requires virtualenv, virtualenvwrapper, and git
#

import os
import random
import re
import shutil
import string
import sys

from subprocess import Popen, call, STDOUT, PIPE

try:
    import argparse
except ImportError:
    print "argparse not installed. Please install with\n"
    print "    sudo pip install argparse\n"
    print "then re-run this script."
    sys.exit(1)


# If user is in a virtualenv, tell them to get out first
if hasattr(sys, 'real_prefix'):
    print "You're already in a virtualenv. Type\n"
    print "    deactivate\n"
    print "to leave, then run this script again."
    sys.exit(1)

VIRTUALENV_WRAPPER_PATH = '/usr/local/bin/virtualenvwrapper.sh'
if not os.path.isfile(VIRTUALENV_WRAPPER_PATH):
    cmd = 'echo $VIRTUALENV_WRAPPER_PATH'
    output = call(cmd, shell=True)
    if output:
        VIRTUALENV_WRAPPER_PATH = output
    else:
        print "We can not seem to find virtualenvwrapper\n"
        print "Either install it through pip\n"
        print "     sudo pip install virtualenvwrapper\n"
        print "or set $VIRTUALENV_WRAPPER_PATH to the location of\n"
        print "virtualenvwrapper on your machine."
        sys.exit(1)

# We have what we need! Let's do this...

DPB_PATH = os.path.abspath(os.path.dirname(__file__)) + '/'
DJANGO_FILES_PATH = DPB_PATH + 'django-files/'

# These are the arguments for the builder.  We can extend the
# arguments as we want to add more functionality
parser = argparse.ArgumentParser(description='''PTM Web Engineering presents
                                 Django Project Builder''')

# Arg to declare the path to where the project will be made
parser.add_argument('--version', '-v', action='version',
                    version='Django Project Builder v0.1')
parser.add_argument('--path', action='store', dest='path',
                    help='''Specifies where the new Django project
                    should be made, including the project name at the
                    end (e.g. /home/username/code/project_name)''',
                    required=True)
# Arg for using bootstrap rather than generic templates/media
parser.add_argument('--bootstrap', action='store_true', default=False,
                    help='''This will include Bootstrap as the template
                    and media base of the project.''', dest='bootstrap')
# Simple ones
parser.add_argument('-q', '--quiet', action='store_true', default=False,
                    help='''Quiets all output except the finish message.''',
                    dest='quiet')


arguments = parser.parse_args()

def check_projectname():
    if not re.search(r'^[_a-zA-Z]\w*$', PROJECT_NAME):
        message = 'Error: \'%s\' is not a valid project name. Please ' %  PROJECT_NAME
        if not re.search(r'^[_a-zA-Z]', PROJECT_NAME):
            message += ('make sure the name begins '
                       'with a letter or underscore.')
        else:
            message += 'use only numbers, letters and underscores.'

    sys.exit(message)

def copy_files(folder_path, file_types, pathify):
    """Copies the contents of django_files and server_scripts, and
    performs string interpolations (e.g., %(APP_NAME)s => 'myapp')"""
    for filename in file_types:
        # Grab *-needed filenames
        f_read = open(folder_path + filename, 'r')
        contents = f_read.read()
        f_read.close()
        # Replace %(SECRET_KEY)s, etc with new value for new project
        if filename.endswith('-needed'):
            new_filename = filename.replace('-needed', '')
        # Loop through list of locations new_filename should be placed
        for dir in pathify[new_filename]:
            # Path names include '%(PROJECT_NAME)s', etc
            file_path = dir % replacement_values
            f_write = open(PROJECT_PATH + file_path + new_filename, 'a')
            new_contents = contents % replacement_values
            f_write.write(new_contents)
            f_write.close()

def sh(cmd):
    return Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE).communicate()[0]

# Maps cleaned filenames to where each file should be copied relative
# to PROJECT_PATH
django_pathify = {
    '.gitignore':                   [''],
    '__init__.py':                  ['%(PROJECT_NAME)s/', '%(APP_NAME)s/'],
    'appurls.py':                   ['%(APP_NAME)s/'],
    'django.wsgi':                  ['apache/'],
    'forms.py':                     ['%(APP_NAME)s/'],
    'manage.py':                    [''],
    'model_forms.py':               ['%(APP_NAME)s/'],
    'models.py':                    ['%(APP_NAME)s/'],
    'requirements.txt':             [''],
    'settings.py':                  ['%(PROJECT_NAME)s/'],
    'settings_local.py':            ['%(PROJECT_NAME)s/'],
    'tests.py':                     ['%(APP_NAME)s/'],
    'urls.py':                      ['%(PROJECT_NAME)s/'],
    'views.py':                     ['%(APP_NAME)s/'],
    'wsgi.py':                      ['%(PROJECT_NAME)s/'],
}

# Trailing / may be included or excluded up to this point
PROJECT_PATH = arguments.path.rstrip('/') + '_site/'
PROJECT_NAME = PROJECT_PATH.split('/')[-2].split('_')[0] # Before the '_site/'
APP_NAME     = PROJECT_NAME + '_app'
BASE_PATH    = '/'.join(PROJECT_PATH.split('/')[:-2]) + '/'

# TODO
# vewrapper = pbs.which('virtualenvwrapper.sh')
# vewrapper("")

SECRET_KEY = ''.join([ random.choice(string.printable[:94].replace("'", ""))
                       for _ in range(50) ])
PROJECT_PASSWORD = ''.join([ random.choice(string.printable[:67].replace("'", ""))
                             for _ in range(30) ])

# Defines key: value pairs so that
#   '%(PROJECT_NAME)s' % replacement_values
# evaluates to the value of the `PROJECT_NAME` variable, such as
#   'my_project_name'
replacement_values = {
    'PROJECT_NAME':     PROJECT_NAME,
    'APP_NAME':         APP_NAME,
    'PROJECT_PASSWORD': PROJECT_PASSWORD,
    'BASE_PATH':        BASE_PATH,
    'SECRET_KEY':       SECRET_KEY,
    'PROJECT_PATH':     PROJECT_PATH,
}

# Doing it this way so DPB can add 'extra_settings' on the fly.
needed_dirs = ['static', 'apache', '%(PROJECT_NAME)s', '%(APP_NAME)s']

# Make sure PROJECT_NAME follows Django's restrictions
check_projectname()

if not arguments.quiet:
    print "Creating directories..."

# Use 'git init' to create the PROJECT_PATH directory and turn it into
# a git repo
cmd = 'bash -c "git init %s"' % PROJECT_PATH
output = sh(cmd)

if not arguments.quiet:
    print '\n', output, '\n'

# Create all other dirs (each a sub-(sub-?)directory) of PROJECT_PATH
for dir_name in needed_dirs:
    os.mkdir(PROJECT_PATH + dir_name % replacement_values)

# Build list of all django-specific files to be copied into new project.
django_files = [x for x in os.listdir(DJANGO_FILES_PATH)
                if x.endswith('-needed')]

if not arguments.quiet:
    print "Creating django files..."

# Oddly-placed '%' in weird_files screws up our string interpolation,
# so copy these files verbatim
copy_files(DJANGO_FILES_PATH, django_files, django_pathify)

if not arguments.quiet:
    print "Copying directories..."

# Add directory names here
generic_dirs = ['media', 'templates']
generic_dirs = [DPB_PATH + d for d in generic_dirs]

for dirname in generic_dirs:
    # cp -r media-generic $PROJECT_PATH/media && cp -r templates-generic ...
    new_dir = PROJECT_PATH + dirname.split('/')[-1]
    if arguments.bootstrap:
        shutil.copytree(dirname + '-bootstrap', new_dir)
    else:
        shutil.copytree(dirname + '-generic', new_dir)

if not arguments.quiet:
    print "Making virtualenv..."

cmd  = 'bash -c "source %s &&' % VIRTUALENV_WRAPPER_PATH
cmd += ' mkvirtualenv %s --no-site-packages"' % PROJECT_NAME

output = sh(cmd)

if not arguments.quiet:
    print '\n', output, '\n'

## The below part is made much faster with a small requirements.txt.
## We have the opitions to include more packages, which in turn
## will take long, but of course is needed. This allows for making
## projects which need only the basics, and ones that need a lot.

if not arguments.quiet:
    print "Running 'pip install -r requirements.txt'. This could take a while...",
    print "(don't press control-c!)"

# FIXME Shouldn't assume the location of virtualenvwrapper.sh
cmd  = 'bash -c "source %s && workon' % VIRTUALENV_WRAPPER_PATH
cmd += ' %(PROJECT_NAME)s && cd %(PROJECT_PATH)s' % replacement_values
cmd += ' && pip install -r requirements.txt"'

output = sh(cmd)

if not arguments.quiet:
    print '\n', output, '\n'

# virtualenv now exists

if not arguments.quiet:
    print "Creating git repo..."

cmd  = 'bash -c "cd %s &&' % PROJECT_PATH
cmd += ' git add . && git commit -m \'First commit\'"'
output = sh(cmd)

if not arguments.quiet:
    print '\n', output, '\n'

print "\nDone! Now run\n"
print "    cd %(PROJECT_PATH)s && workon %(PROJECT_NAME)s &&" % replacement_values,
print "python manage.py syncdb\n\nGet to work!"
