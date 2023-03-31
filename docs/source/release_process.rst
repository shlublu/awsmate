Release process
===============

* Create a new branch named after the next version number "9.9.9"
* Set this version number in
   * ``/pyproject.toml``: ``version = "x.y.z"``
   * ``/src/awsmate/__init.py__``: ``__version__ = 'x.y.z'``
   * ``Changelog``: new empty section
* Set the project's development status classifier in ``/pyproject.toml``
* ...do the job...
* ...test the job...
* Update the changelog, including the release date
* PR and merge into master
* Set commit tag
* PyPi release: as per https://packaging.python.org/en/latest/tutorials/packaging-projects/
   * python3 -m pip install --upgrade build
   * python3 -m build
   * python3 -m pip install --upgrade twine
   * python3 -m twine upload dist/awsmate-<version>* (use __token__)
* Readthedocs: maintain versions (help in https://docs.readthedocs.io/en/stable/tutorial/)
