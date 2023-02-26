# Configuration file for the Sphinx documentation builder.

import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath('..'))

# -- Project information
project = 'awsmate'
copyright = f'{datetime.now().year}, Vincent Poulain (shlublu)'
author = 'shlublu'

# -- General configuration

extensions = [
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'myst_parser'
]

source_suffix = {
    '.py': 'restructuredtext',
    '.md': 'markdown'
}

master_doc = "README.md"
