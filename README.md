PTM Web Engineering's Django Project Builder
============================================

## Intro

Django Project Builder is the fastest, easiest way to, well... build a
new Django project!


## Features and Benefits

* Create a new Django project, git repo, virtualenv, and Django app
  with sane defaults _all_ with a single command

* Prepare your server for deployment with a couple more commands

* Auto-deploy your shiny new Django app to your server with a simple
  `git push`!  (Uses git hooks behind the scenes... but you don't need
  to worry about that, do you?)


## What you don't have to dread anymore

* Tediously editing config files before anything works, even though
  you use the same defaults every single time

* Being forced to copy/paste/edit the same content over and over from
  old `settings.py` files

* Spending too much time configurationating, and not enough time
  coding


## Who is DPB for?

Django programmers looking to do more coding and less config.

For those looking to enjoy convenient server deployments, note that
the server scripts currently assume you're using Bash + virtualenv +
virtualenvwrapper + Ubuntu + Apache.  We're working on reducing the
number of dependencies.

[See our TODO](https://github.com/prototypemagic/django-projectbuilder/blob/master/TODO.md)
for what's on the horizon, and for what you may want to help out with.


## So... how do I use it?

### Dev Box Usage

After cloning this repo to your local machine, `cd` into it and run
something like

    python djangobuilder.py --path ~/new_project

to create the `~/new_project_site` directory, which contains _tons_ of
Django boilerplate -- common imports, virtualenv creation, a new git
repo, and more!

If you add the optional `--bootstrap` argument

    python djangobuilder.py --path ~/new_project --bootstrap

your project will come with all needed bootstrap defaults. In
`media/css/style.css` you will find lots more goodies :-).

`virtualenv` and `virtualenvwrapper` are required. `git` is
recommended. Django is awesome.


### Server Usage

After cloning this repo to one of your many servers, `cd` into it and
run

    bash gitbuilder.sh ~/new_project

to create the top-level project directory, bare git repo, and empty
${PROJECT_NAME}_site directory for the soon-to-exist Django project.
Follow the instructions echoed to the screen, which include using
`apachebuilder.sh` to generate your project's Apache config.

Enjoy!


## Troubleshooting

### Postgres

On Ubuntu, install Postgres with

    sudo apt-get install postgresql-server-dev-all

To install `psycopg2`, Django's Postgres driver, run

    pip install psycopg2

If you get the following error when trying to install Postgres

    ./psycopg/psycopg.h:30:20: fatal error: Python.h: No such file or directory
    compilation terminated.
    error: command 'gcc' failed with exit status 1

that means you haven't installed all the necessary header (*.h) files
to compile additional Python modules/Django apps.  On Ubuntu, run

    sudo apt-get install python-dev

to fix this issue, then again try running

    pip install psycopg2

from within your project's virtualenv to install `psycopg2`.


#### Postgres + Heroku

Heroku requires that you use Postgres as your database.  To install
Postgres, run

    pip install psycopg2

then add `psycopg2` and every other Python module and Django app in
your virtualenv to `requirements.txt` with

    pip freeze > requirements.txt

You'll now want to add `requirements.txt` to your git repo, then
redeploy with

    git add requirements.txt
    git commit -m "Updated requirements.txt"
    git push heroku master

See
[Getting Started with Django on Heroku/Cedar](https://devcenter.heroku.com/articles/django)
with more on deploying to Heroku.

If you run into any other issues, please let us know!
