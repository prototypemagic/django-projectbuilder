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


# TODO once we have made more improvements
- Use distutils to make a setup.py
- Get onto PyPI


# POSSIBLE TODO's
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
