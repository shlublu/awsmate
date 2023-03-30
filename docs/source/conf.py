# Configuration file for the Sphinx documentation builder.

import os
import sys

from datetime import datetime

from awsmate import __version__

sys.path.insert(0, os.path.abspath('../../src'))

# -- Project information -----------------------------------------------------

project = 'awsmate'
copyright = f"{datetime.now().year}, Vincent Poulain (shlublu)"
author = 'shlublu'

# The full version, including alpha/beta/rc tags
release = __version__

# -- General configuration ---------------------------------------------------

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

templates_path = ['_templates']

root_doc = "index"

# -- Options for HTML output -------------------------------------------------

toc_object_entries_show_parents = 'hide'

html_static_path = ['_static']

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
    # Toc options
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# -- Extension configuration -------------------------------------------------

# Autodoc settings
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

# Napoleon settings
napoleon_google_docstring = False
napoleon_numpy_docstring = True

# Toolbox Github settings
github_username = author
github_repository = project