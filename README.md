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

* Code rollbacks: use Fabric? Or will `git revert master~2..master` do?

* Add to and tidy up CREDITS.md


## SBHX Presentation-inspired TODO

* djangobuilder.py: 'git init $PROJECT_NAME' instead of 'mkdir $PROJECT_NAME'

* djangobuilder.py: Create initial commit on client

* djangobuilder.py: fix bug preventing .gitignore-generic from being copied

* djangobuilder.py: When running migration on newly-created project (on user's dev box), use http://www.arthurkoziel.com/2008/09/04/automatical-superuser-creation-django/ to automate superuser creation

* Create postgresbuilder.sh for automatic Postgres user creation, credentials included

* gitbuilder.sh: chmod 777 $PROJECT_NAME and $PROJECT_NAME/${PROJECT_NAME}_site :-\

* Integrate Bootstrap

* Integrate LessCSS

* Create route53builder.py to automatically create new subdomain [NOTE: I'll use the script Jay wrote for Cazooz]