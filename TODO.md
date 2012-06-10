# TODO
- Write README
- Write Quick Start docs
- Use stdin/out/err pipes to show output during `pip install -r requirements.txt`
- Fix `cpvirtualenv` bug in `virtualenvwrapper.sh` or create our own replacement
- Ensure the existence of all programs used
  - E.g., pip, virtualenv, virtualenvwrapper, bash, git
- Create and use the `dpb-default` virtualenv
- Add `python manage.py migrate` to server's git hooks
- Server should use something like `lynx -dump checkip.dyndns.org 2>&1 | awk '{print $4}' | grep ^[0-9]` in place of the generic `my-django-powered-site.com`
- Create `postgresbuilder.sh` or equivalent
<<<<<<< HEAD
- Use fixtures to createsuperuser
=======
- Tell user _not_ to create virtualenv (we do it for them!)
- If user is in a virtualenv, get out of it before executing `djangobuilder.sh`

>>>>>>> master

# TODO once we have made more improvements
- Use distutils to make a setup.py
- Get onto PyPI


# POSSIBLE TODOs
- Re-write server scripts using argparse
- Combine the server scripts into one program


# Completed
- Add Bootstrap and Non-Bootstrap options
- Make it so everything can be relative rather than absolute
- Make more files generic
- Clean up files
- Organize folders
- Write Contributors
- Write Credits
