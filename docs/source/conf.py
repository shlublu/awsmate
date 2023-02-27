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
release = '0.0.2'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'myst_parser',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown'
}

root_doc = "index"

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'

# -- Extension configuration -------------------------------------------------

# Napoleon settings
napoleon_google_docstring = False
napoleon_numpy_docstring = True


