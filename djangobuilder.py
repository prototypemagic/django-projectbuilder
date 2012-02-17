#!/usr/bin/env python
# Steve Phillips / elimisteve
# 2012.01.28

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
                    to where the project should be made''')
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


# FIXME Every file in generic_scripts and *-generic should be listed
# here... or we can copy entire directories
pathify = {
    '.gitignore':        ['%(PROJECT_NAME)s/'],
    '__init__.py':       ['', '%(PROJECT_NAME)s/', 'extra_settings/'],
    'django.wsgi':       ['apache/'],
    'manage.py':         [''],
    'model_forms.py':    ['%(PROJECT_NAME)s/'],
    'models.py':         ['%(PROJECT_NAME)s/'],
    'requirements.txt':  [''],
    'settings.py':       [''],
    'settings_local.py': [''],
    'tests.py':          ['%(PROJECT_NAME)s/'],
    'urls.py':           [''],
    'views.py':          ['%(PROJECT_NAME)s/'],
}
weird_files = ['manage.py']

#These will check whether the user used --zinnia or --cms and
#if so will add the needed settings.
if arguments.cms == True or arguments.zinnia == True:
    pathify.update({'cms_settings.py' : [''],})
if arguments.zinnia == True:
    pathify.update({'zinnia_settings.py' : [''],})

HOME_DIR = os.path.expandvars('$HOME').rstrip('/') + '/'

# Trailing / may be included or excluded
PROJECT_PATH = arguments.path.rstrip('/') + '_site/'
PROJECT_NAME = PROJECT_PATH.split('/')[-2].split('_')[0] # Before the '_site/'
BASE_PATH    = '/'.join(PROJECT_PATH.split('/')[:-2]) + '/'

# FIXME Shouldn't assume the location of virtualenvwrapper.sh
print "Making virtualenv..."
cmd  = 'bash -c "source /usr/local/bin/virtualenvwrapper.sh'
cmd += ' && mkvirtualenv %s --no-site-packages"' % (PROJECT_NAME)
status, output = commands.getstatusoutput(cmd)
print
print output
print

# TODO
# vewrapper = pbs.which('virtualenvwrapper.sh')
# vewrapper("")

SECRET_KEY = ''.join([ random.choice(string.printable[:94].replace("'", ""))
                       for _ in range(50) ])
PROJECT_PASSWORD = ''.join([ random.choice(string.printable[:67].replace("'", ""))
                             for _ in range(30) ])

replacement_values = {
    'PROJECT_NAME':     PROJECT_NAME,
    'PROJECT_PASSWORD': PROJECT_PASSWORD,
    'BASE_PATH':        BASE_PATH,
    'SECRET_KEY':       SECRET_KEY,
    'PROJECT_PATH':     PROJECT_PATH,
}


print "Creating directories..."
for dir_name in ['', 'static', 'apache', 'extra_settings',
                 '%(PROJECT_NAME)s']:
    os.mkdir(PROJECT_PATH + dir_name % replacement_values)


generic_files = [x for x in os.listdir(GENERIC_SCRIPTS_PATH)
                 if x.endswith('-generic')]

#This adds cms_settings/zinnia_settings
#to generic_files.
##FIXME shouldn't be hard coded
#if arguments.cms == True or arguments.zinnia == True:
#    extra_files = [x for x in os.listdir('extra_settings/')
#                      if x.startswith('cms')]
#if arguments.zinnia == True:
#    extra_files += [x for x in os.listdir('extra_settings/')
#                      if x.startswith('zinnia')]


print "Creating files..."
for filename in generic_files:
    # Grab *-generic filenames
    f_read = open(GENERIC_SCRIPTS_PATH + filename, 'r')
    contents = f_read.read()
    f_read.close()

    # Replace %(SECRET_KEY)s, etc with new value for new project
    new_filename = filename.replace('-generic', '')
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


print "Copying directories..."
generic_dirs = ['media', 'templates']
for dirname in generic_dirs:
    # cp -r media-generic $PROJECT_PATH/media && cp -r templates-generic ...
    ### FIXME: Assumes script is being run from the directory it's in
    shutil.copytree(dirname + '-generic', PROJECT_PATH + dirname)

print "Running 'pip install -r requirements.txt'. This could take a while..."
cmd  = 'bash -c "source /usr/local/bin/virtualenvwrapper.sh && '
cmd += 'workon %(PROJECT_NAME)s && cd %(PROJECT_PATH)s && pip install -r requirements.txt"' % \
    replacement_values
status, output = commands.getstatusoutput(cmd)
print
print output
print
print "Done! Now run  \n\n    cd %(PROJECT_PATH)s && workon %(PROJECT_NAME)s\n\nGet to work!" % replacement_values
