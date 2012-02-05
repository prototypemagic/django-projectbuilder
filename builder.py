#!/usr/bin/env python
# Steve Phillips / elimisteve
# 2012.01.28

#
# Requires fabric, virtualenv, and virtualenvwrapper
#

# FIXME This shouldn't be hard-coded
GENERIC_SCRIPTS_PATH = 'generic_scripts/'

#import pbs
import commands, os, random, string, sys

USAGE = '%s /path/to/new/project_name' % (sys.argv[0])
FUTURE_USAGE = USAGE + ' [--cms] [--zinnia]'

if len(sys.argv) < 2:
    print USAGE
    sys.exit(0)

# FIXME Every file in generic_scripts and *-generic should be listed
# here... or we can copy entire directories
pathify = {
    '.gitignore':        ['%(PROJECT_NAME)s/'],
    '__init__.py':       ['%(PROJECT_NAME)s/', 'extra_settings/'],
    'cms_settings.py':   ['extra_settings/'],
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
    'zinnia_settings.py':['extra_settings/'],
}
weird_files = ['manage.py']

HOME_DIR = os.path.expandvars('$HOME').rstrip('/') + '/'

# Trailing / may be included or excluded
PROJECT_PATH = sys.argv[1].rstrip('/') + '/'
PROJECT_NAME = PROJECT_PATH.split('/')[-2]
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
}


print "Creating directories..."
for dir_name in ['', 'media', 'static', 'templates', 'apache', 'extra_settings',
                 '%(PROJECT_NAME)s']:
    os.mkdir(PROJECT_PATH + dir_name % replacement_values)


generic_files = [x for x in os.listdir(GENERIC_SCRIPTS_PATH)
                 if x.endswith('-generic')]


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


print "Running 'pip install -r requirements.txt'. This could take a while..."
cmd  = 'bash -c "source /usr/local/bin/virtualenvwrapper.sh && '
cmd += 'workon %(PROJECT_NAME)s && cd %(PROJECT_NAME)s && pip install -r requirements.txt"' % \
    replacement_values
status, output = commands.getstatusoutput(cmd)
print 
print output
print
print "Done! Now run 'cd %(PROJECT_NAME)s && workon %(PROJECT_NAME)s'.\nGet to work!" % replacement_values
