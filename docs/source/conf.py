# Configuration file for the Sphinx documentation builder.

import os
import sys

from datetime import datetime

sys.path.insert(0, os.path.abspath('../../src'))

# -- Project information -----------------------------------------------------

project = 'awsmate'
copyright = f"{datetime.now().year}, Vincent Poulain (shlublu)"
author = 'shlublu'

# The full version, including alpha/beta/rc tags
release = '0.0.3'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx_toolbox.github',
    'sphinx_toolbox.sidebar_links',
    'myst_parser'
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown'
}

root_doc = "index"

autoclass_content = "both"

autodoc_default_options = {
    "undoc-members": False,
    "members": True,
    "private-members": False,
    "inherited-members": False,
    "special-members": False,
    "undocumented-members": False,
    "show-inheritance": True,
    "member-order": "bysource",
}

toc_object_entries_show_parents = 'hide'

github_username = author
github_repository = project

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'navigation_depth': 5
}

# -- Extension configuration -------------------------------------------------

# Napoleon settings
napoleon_google_docstring = False
napoleon_numpy_docstring = True
