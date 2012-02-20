#!/usr/bin/env python

#
# Requires fabric, virtualenv, and virtualenvwrapper
#

# FIXME This shouldn't be hard-coded
GENERIC_SCRIPTS_PATH = 'generic_scripts/'

#import pbs
import commands, os, random, shutil, string, sys, argparse

USAGE = 'usage: %s [-h] [-v] [--path PATH] [--cms | --zinnia]' % (sys.argv[0])
#FUTURE_USAGE = USAGE + ' [--cms] [--zinnia]'

if len(sys.argv) < 2:
    print USAGE
    sys.exit(0)

# These are the arguements for the builder
# We can extent the arguements as we want to add
# more diversity
parser = argparse.ArgumentParser(description='''ProtoType Magic presents
                                  Django Project Builder and so much more...''',
                                  version='djangbuilder.py 0.2.3')
parser.add_argument('--path', action='store', dest='path',
                    help='''Use this to direct Django Project Builder
                    to where the project should be made, including
                    the project name at the end. e.g. /home/username/project_name''')
# This makes it so we don't derp and use --zinnia and --cms
cms_options = parser.add_mutually_exclusive_group()
cms_options.add_argument('--cms', action='store_true', default=False,
                         help='''This will include Django-CMS along with all
                         typically used packages.''', dest='cms'
                         )
cms_options.add_argument('--zinnia', action='store_true', default=False,
                         help='''This will include Zinnia (along with Django-CMS)
                         and all the needed files and required packages.''',
                         dest='zinnia'
                         )
# This allows for ease of checking whether
# either --zinnia or --cms was used
arguments = parser.parse_args()


# FIXME Every file in generic_scripts and *-needed should be listed
# here... or we can copy entire directories
pathify = {
    '.gitignore':        ['%(PROJECT_NAME)s/'],
    '__init__.py':       ['', '%(PROJECT_NAME)s/'],
    'django.wsgi':       ['apache/'],
    'manage.py':         [''],
    'model_forms.py':    ['%(PROJECT_NAME)s/'],
    'models.py':         ['%(PROJECT_NAME)s/'],
    'requirements.txt':  [''],
    'settings.py':       [''],
    'settings_local.py': [''],
    'settings_local.py-local': [''],
    'tests.py':          ['%(PROJECT_NAME)s/'],
    'urls.py':           [''],
    'views.py':          ['%(PROJECT_NAME)s/'],
}

#These will check whether the user used --zinnia or --cms and
#if so will add the needed settings.
if arguments.cms or arguments.zinnia:
    pathify.update({'cms_settings.py' : [''],})
    pathify.update({'__init__.py': ['', '%(PROJECT_NAME)s/', 'extra_settings/'],})
if arguments.zinnia:
    pathify.update({'zinnia_settings.py' : [''],})

HOME_DIR = os.path.expandvars('$HOME').rstrip('/') + '/'

# Trailing / may be included or excluded
PROJECT_PATH = arguments.path.rstrip('/') + '_site/'
PROJECT_NAME = PROJECT_PATH.split('/')[-2].split('_')[0] # Before the '_site/'
BASE_PATH    = '/'.join(PROJECT_PATH.split('/')[:-2]) + '/'

# FIXME Shouldn't assume the location of virtualenvwrapper.sh

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
    'PROJECT_PASSWORD': PROJECT_PASSWORD,
    'BASE_PATH':        BASE_PATH,
    'SECRET_KEY':       SECRET_KEY,
    'PROJECT_PATH':     PROJECT_PATH,
}

# Doing it this way so DPB can add 'extra_settings' on the fly.
needed_dirs = ['static', 'apache', '%(PROJECT_NAME)s']

if arguments.cms or arguments.zinnia:
    needed_dirs += ['extra_settings']

print "Creating directories..."

# Let 'git init' create the PROJECT_PATH directory and turn it into a
# git repo with one command
cmd = 'bash -c "git init %s"' % PROJECT_PATH
_, output = commands.getstatusoutput(cmd)
print '\n', output, '\n'

# Create all other dirs (each a sub-(sub-?)directory) of PROJECT_PATH
for dir_name in needed_dirs:
    os.mkdir(PROJECT_PATH + dir_name % replacement_values)


generic_files = [x for x in os.listdir(GENERIC_SCRIPTS_PATH)
                 if x.endswith('-needed')]

if arguments.cms or arguments.zinnia:
    generic_files.remove('urls.py-needed')
    generic_files += [x for x in os.listdir(GENERIC_SCRIPTS_PATH)
                      if x.endswith('-cms')]

# Oddly-placed '%' in weird_files screws up our string interpolation,
# so copy these files verbatim
weird_files = ['manage.py']

print "Creating files..."
for filename in generic_files:
    # Grab *-needed filenames
    f_read = open(GENERIC_SCRIPTS_PATH + filename, 'r')
    contents = f_read.read()
    f_read.close()

    # Replace %(SECRET_KEY)s, etc with new value for new project
    if filename.endswith('-needed'):
        new_filename = filename.replace('-needed', '')
    if filename.endswith('-cms'):
        new_filename = filename.replace('-cms', '')
    # Loop through list of locations new_filename should be placed
    for dir in pathify[new_filename]:
        # Path names include '%(PROJECT_NAME)s', etc
        file_path = dir % replacement_values
        f_write = open(PROJECT_PATH + file_path + new_filename, 'a')

        if new_filename not in weird_files:
            new_contents = contents % replacement_values
        else:
            new_contents = contents
        f_write.write(new_contents)
        f_write.close()


# Adds cms_settings/zinnia_settings
# FIXME shouldn't be hard coded
if arguments.cms or arguments.zinnia:
    shutil.copy('extra_settings/cms_settings.py',
                PROJECT_PATH + 'extra_settings/')

if arguments.zinnia:
    shutil.copy('extra_settings/zinnia_settings.py',
                PROJECT_PATH + 'extra_settings/')


print "Copying directories..."

generic_dirs = ['media', 'templates']

for dirname in generic_dirs:
    # cp -r media-generic $PROJECT_PATH/media && cp -r templates-generic ...
    ### FIXME: Assumes script is being run from the directory it's in
    if arguments.zinnia or arguments.cms:
        shutil.copytree(dirname + '-cms', PROJECT_PATH + dirname)
    else:
        shutil.copytree(dirname + '-generic', PROJECT_PATH + dirname)


## Making the virtualenv here

print "Making virtualenv..."
cmd = ''
cmd = 'bash -c "source /usr/local/bin/virtualenvwrapper.sh &&'
cmd += ' mkvirtualenv %s --no-site-packages"' % PROJECT_NAME

_, output = commands.getstatusoutput(cmd)
print '\n', output, '\n'

## The below part is made much fast with a small requirements.txt.
## We have the opitions to include more packages, which in turn
## will take long, but of course is needed. This allows for making
## projects which need only the basic's, and ones that need a lot.

cmd = ''
print "Running 'pip install -r requirements.txt'. This could take a while..."
# FIXME Shouldn't assume the location of virtualenvwrapper.sh
cmd  = 'bash -c "source /usr/local/bin/virtualenvwrapper.sh && workon'
cmd += ' %(PROJECT_NAME)s && cd %(PROJECT_PATH)s' % replacement_values
cmd += ' && pip install -r requirements.txt"'

_, output = commands.getstatusoutput(cmd)
print '\n', output, '\n'

#Now virtualenv exists

cmd = ''
if arguments.zinnia or arguments.cms:
    print "Installing Django-CMS..."
    cmd  = 'bash -c "source /usr/local/bin/virtualenvwrapper.sh && workon %s' \
        % PROJECT_NAME
    cmd += ' && pip install django-cms"'
    _, output = commands.getstatusoutput(cmd)
    print '\n', output, '\n'

cmd = ''
if arguments.zinnia:
    print "Installing Zinnia..."
    cmd  = 'bash -c "source /usr/local/bin/virtualenvwrapper.sh && workon %s' \
        % PROJECT_NAME
    cmd += ' && pip install django-blog-zinnia"'
    _, output = commands.getstatusoutput(cmd)
    print '\n', output, '\n'


# Run 'cpvirtualenv PROJECT_NAME default' ?
#if ask_to_copy_default_virtualenv:
#    q = "Create a default virtualenv to speed this up next time? " % PROJECT_NAME
#    answer = raw_input(q)
#    if answer and answer.lower()[0] == 'y':
#        print "Copying virtualenv..."
#        cmd  = 'bash -c "source /usr/local/bin/virtualenvwrapper.sh && workon '
#        cmd += '%(PROJECT_NAME)s && cpvirtualenv %(PROJECT_NAME)s default --no-site-packages"' % \
#            replacement_values
#        _, output = commands.getstatusoutput(cmd)
#        print '\n', output, '\n'

print "Creating git repo..."
cmd  = 'bash -c "cd %s &&' % PROJECT_PATH
cmd += ' git add . && git commit -m \'First commit\'"'
_, output = commands.getstatusoutput(cmd)
print '\n', output, '\n'

print "Done! Now run\n"
print "    cd %(PROJECT_PATH)s && workon %(PROJECT_NAME)s &&" % replacement_values,
print "python manage.py syncdb\n\nNow get to work!"
