### Release process

* Create a new branch named after the next version number "v9.9.9"
* Set this version number 
    - /pyproject.toml: `version = "x.y.z"`
    - /docs/sources/conf.py: `release = 'x.y.z'`
* Set the project's development status classifier in /pyproject.toml
* ...do the job...
* ...test the job...
* Merge into master
* Set commit tag
* PyPi release: https://packaging.python.org/en/latest/tutorials/packaging-projects/
* Readthedocs: https://docs.readthedocs.io/en/stable/tutorial/

### Todo before writing new code

* Automation
  - Autodeploy on PyPi when merging into master (CI task)
  - Autogenerate ReadTheDocs when merging to master (ReadTheDocs merge listener)
  - Set commit tag when merging into master (CI task)
  - Automatize step "Set this version number" above when creating a new version branch
* Documentation 
  - Finish documenting the existing code
  - Create proper sections: https://realpython.com/documenting-python-code/#public-and-open-source-projects
  - Add a changelog
  - Set the changelog URL: /pyproject.toml: `[project.urls]` 
  - Enable versions: https://docs.readthedocs.io/en/stable/tutorial/
  