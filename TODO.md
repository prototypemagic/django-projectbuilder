# TODO
- Make server scripts less (read: not) dependent upon...
  - Ubuntu
  - The location of `virtualenvwrapper.sh`
  - Apache
  - Bash
- Rewrite DPB to either use Django itelf to render project files, or at least generate new projects the way Django does
  - E.g., render something like `{{ project_name }}` instead of using `%(PROJECT_NAME)s`
- Add modular support for non-`git` source control (`hg`, `bzr`, etc) system
- Use stdin/out/err pipes to show output during `pip install -r requirements.txt`
- Ensure the existence of all required programs
  - E.g., pip, virtualenv, virtualenvwrapper, bash, and preferably git
- Add `python manage.py migrate` to server's git hooks
- Server should use something like `lynx -dump checkip.dyndns.org 2>&1 | awk '{print $4}' | grep ^[0-9]` in place of the generic `my-django-powered-site.com`
- Create `postgresbuilder.sh` or equivalent
- Fix `cpvirtualenv` bug in `virtualenvwrapper.sh` or create our own replacement
  - Create the `dpb-default` virtualenv, then copy it when creating new projects
    - `cp -r ~/.virtualenvs/dpb-default ~/.virtualenvs/NEW_PROJECT_NAME`
    - Replace `#!/home/username/.virtualenvs/dpb-default/bin/python` with `#!/home/username/.virtualenvs/NEW_PROJECT_NAME/bin/python`
- Add above TODO items to GitHub's ticketing system

# Possible TODO
- Re-write server scripts using argparse
- Combine the server scripts into one program

# Future TODO
- Use `distutils` to make a `setup.py`
- Deploy DPB to PyPI

# Completed
- Add Bootstrap and non-Bootstrap options
- Make it so everything can be relative rather than absolute
- Make more files generic
- Clean up files
- Organize folders
- Write Contributors
- Write Credits
- If user is in a virtualenv, get out of it (or tell them to) before executing `djangobuilder.py`
- Tell user _not_ to create virtualenv (we do it for them!)
- Write README
- Write Quick Start docs
- Much more
