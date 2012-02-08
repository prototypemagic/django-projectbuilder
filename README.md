ProtoType Magic's Django Project Builder
========================================

## Usage

After cloning this repo, cd into it then run

    bash gitbuilder.sh /path/to/new_project

to create the "top-level" directory and bare git repo for the about-to-exist Django project.  Then run

    python builder.sh /path/to/new_project/new_project

to create the /path/to/new_project/new_project_site directory, which contains lots of Django boilerplate -- common imports, virtualenv creation + the Django apps/Python modules we always install (Django, South, Celery, django-cms, etc), and even HTML5 Boilerplate.


## TODO

* settings.py: From SQLite to Postgres

* post-receive: Run Postgres migrations

* Database rollbacks: create timestamped SQL dump before migrations, then rollback with a post-receive commit?

* builder.py: Copy media-generic/ and templates-generic/ to appropriate place

* proto-new-virtualhost-subdomain.py: Give user command to create sites-available Apache config and sites-enabled symlink

* Code rollbacks: use Fabric? Or will `git revert master~2..master` do?
