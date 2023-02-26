# Configuration file for the Sphinx documentation builder.

# -- Project information
from datetime import datetime

project = 'awsmate'
copyright = f'{datetime.now().year}, Vincent Poulain (shlublu)'
author = 'shlublu'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.py': 'numpy',
    '.md': 'markdown',
}

master_doc = "index.md"
