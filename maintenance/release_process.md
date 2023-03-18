* Create a new branch named after the next version number "9.9.9"
* Set this version number 
    - /pyproject.toml: `version = "x.y.z"`
    - /docs/sources/conf.py: `release = 'x.y.z'`
* Set the project's development status classifier in /pyproject.toml
* ...do the job...
* ...test the job...
* Update the changelog, including the release date
* PR and merge into master
* Set commit tag
* PyPi release: https://packaging.python.org/en/latest/tutorials/packaging-projects/
* Readthedocs: https://docs.readthedocs.io/en/stable/tutorial/
