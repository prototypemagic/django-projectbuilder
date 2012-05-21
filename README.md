ProtoType Magic's Django Project Builder
========================================

## Dev Box Usage

After cloning this repo, `cd` into it and run

    python djangobuilder.py --path /path/to/newproject [--bootstrap] 

to create the /path/to/newproject_site directory, which
contains lots of Django boilerplate -- common imports, virtualenv
creation.

If you add the --bootstrap arguement, your project will come with all
needed bootstrap defaults. In media/css/style.css there are also a lot
of goodies.


## Server Usage

After cloning this repo, `cd` into it and run

    bash gitbuilder.sh /path/to/new_project

to create the "top-level" directory, bare git repo, and empty
${PROJECT_NAME}_site directory for the soon-to-exist Django project.
Follow the instructions provided, which include using apachebuilder.sh
to generate your project's Apache config.
