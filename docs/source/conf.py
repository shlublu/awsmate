# Configuration file for the Sphinx documentation builder.

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(".."))

# -- Project information

project = "awsmate"
copyright = f"{datetime.now().year}, Vincent Poulain (shlublu)"
author = "shlublu"

# -- General configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_parser",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

master_doc = "README.md"
