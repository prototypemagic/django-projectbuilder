ProtoType Magic's Django Project Builder
========================================

## Server Usage

After cloning this repo, `cd` into it and run

    bash gitbuilder.sh /path/to/new_project

to create the "top-level" directory, bare git repo, and empty
${PROJECT_NAME}_site directory for the soon-to-exist Django project.
Follow the instructions provided, which include using apachebuilder.sh
to generate your project's Apache config.


## Dev Box Usage

After cloning this repo, `cd` into it and run

    python djangobuilder.py new_project

to create the /path/to/new_project/new_project_site directory, which
contains lots of Django boilerplate -- common imports, virtualenv
creation + the Django apps/Python modules we always install (Django,
South, Celery, django-cms, etc), and even HTML5 Boilerplate.


## TODO

* settings.py: From SQLite to Postgres

* post-receive: Run Postgres migrations

* Database rollbacks: create timestamped SQL dump before migrations, then rollback with a post-receive commit?

* Code rollbacks: use Fabric? Or is `git revert master~2..master` good enough?

* Add to and tidy up CREDITS.md

* Start using Django Compressor

## SBHX Presentation-inspired TODO

* djangobuilder.py: When running first migration on newly-created project (on user's dev box), use http://www.arthurkoziel.com/2008/09/04/automatical-superuser-creation-django to automate superuser creation

* djangobuilder.py: fix bug preventing .gitignore-generic from being copied into new repo

* Create postgresbuilder.sh for automatic Postgres user creation, credentials included

* Create route53builder.py to automatically create new subdomain [NOTE: I'll use the script Jay wrote for Cazooz]

* Integrate Bootstrap

* Integrate LessCSS

## Front End Options
(We will usually use Bootstrap, so these are all things that can come into
play "underneath" bootstrap
* ajvb's boilerplate style.css, which takes heavy influence from HTML5BP
* HTML5BP
    *The older version
    *The newer version

The plan is for there to be cmd line arg's for different options, where the
typical will be Bootstrap + ajvb's custom style.css, which is a mixed of old
and new H5BP, as well as his own default class's, bootstrap changes, etc. 

###Later Changes to /media/
Also there 'might' be other options for Zinnia, Django-CMS, etc. Not sure yet.

