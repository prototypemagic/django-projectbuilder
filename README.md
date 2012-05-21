PTM Web Engineering's Django Project Builder
============================================

## Intro

Django Project Builder is the fastest, easiest way to, well... build a
new Django project!


## Features

* Create a new Django project, git repo, virtualenv, and Django app
  with sane defaults _all_ with a single command

* Prepare your server to be deployed to with a couple more commands

* Auto-deploy your shiny new Django app to your server with a simple
  `git push`!  (Uses git hooks behind the scenes... but you don't need
  to worry about that, do you?)


## Non-features

* Tediously editing config files before anything works, even though
  you use the same defaults every single time

* Being forced to copy/paste/edit the same content over and over from
  old `settings.py` files

* Spending too much time configurationating, and not enough time
  coding


## Usage

### Dev Box Usage

After cloning this repo, `cd` into it and run

    python djangobuilder.py --path /path/to/newproject [--bootstrap]

to create the /path/to/newproject_site directory, which contains
_tons_ of Django boilerplate -- common imports, virtualenv creation,
new git repo, and more!

If you add the `--bootstrap` argument, your project will come with all
needed bootstrap defaults. In `media/css/style.css` you will find lots
more goodies :-).

git, virtualenv, virtualenvwrapper, and bash are required.


### Server Usage

After cloning this repo, `cd` into it and run

    bash gitbuilder.sh /path/to/new_project

to create the "top-level" directory, bare git repo, and empty
${PROJECT_NAME}_site directory for the soon-to-exist Django project.
Follow the instructions provided, which include using `apachebuilder.sh`
to generate your project's Apache config.
