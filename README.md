ProtoType Magic's Django Project Builder
========================================

## TODO

* Relativize paths ("PROJECT_ROOTify")

*


## Tips for Soon/Later

    import commands, os, random, string

    pathify = {
        'settings.py':       '',
        'settings_local.py': '',
        'urls.py':           '',
        'urls_dev.py':       '',
        'django.wsgi':       'apache/',
    }

    PROJECT_NAME = raw_input()  # Will be different for Django
    #BASE_PATH    = '/home/ubuntu/django_projects/'    #
    BASE_PATH    = '/home/steve/dpc/proto/'            # Why not use os.path?
    PROJECT_ROOT = BASE_PATH + PROJECT_NAME            #

    # Make virtualenv
    ###status, output = commands.getstatusoutput()
    VIRTUALENV_PATH = BASE_PATH + '.virtualenvs/' + PROJECT_NAME

    # Make directories
    for dir_name in ['', 'media', 'static', 'templates']:
        os.mkdir(dir_name)

    #GENERIC_SCRIPTS_PATH = BASE_PATH + 'proto-django-projectbuilder/generic_scripts/'
    GENERIC_SCRIPTS_PATH = BASE_PATH + 'proto-django-projectbuilder/generic_scripts/'

    SECRET_KEY = ''.join([ random.choice(string.printable[:94].replace("'", "")) for _ in range(50) ])

    replacement_values = {
        'PROJECT_NAME':   PROJECT_NAME,
        'BASE_PATH':      BASE_PATH,
        'SECRET_KEY':     SECRET_KEY,
    }

    generic_files = [x for x in os.listdir(GENERIC_SCRIPTS_PATH) if x.endswith('-generic')]

    for filename in generic_files:
        # Grab *-generic filenames
        f_read = open(GENERIC_SCRIPTS_PATH + filename, 'r')
        contents = f.read()
        f.close()

        # Replace %(SECRET_KEY)s, etc with new value for new project
        new_filename = filename.replace('-generic', '')
        f_write = open(PROJECT_ROOT + pathify[new_filename], 'w')
        new_contents = contents % replacement_values
        f_write.write(new_contents)
        f_write.close()
