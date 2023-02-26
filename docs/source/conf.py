# Configuration file for the Sphinx documentation builder.

# -- Project information
from datetime import datetime

project = 'awsmate'
copyright = f'{datetime.now().year}, Vincent Poulain (shlublu)'
author = 'shlublu'

# -- General configuration

extensions = [
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon'
]

source_suffix = {
    '.py': 'restructuredtext',
    '.md': 'markdown'
}

master_doc = "index"
