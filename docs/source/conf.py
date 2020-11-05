# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

import django

sys.path.insert(0, os.path.abspath('../..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'SimpleVPN.settings.development'

django.setup()


# -- Project information -----------------------------------------------------

project = 'SimpleVPN'
copyright = '2020, Alessandro Romani'
author = 'Alessandro Romani'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'recommonmark',
    'sphinxcontrib_django',
    'sphinx_copybutton',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

typehints_document_rtype = False

add_module_names = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_material'

html_favicon = "images/favicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    'css/color.css',
]


html_theme_options = {
    'nav_title': 'SimpleVPN Server',
    'base_url': 'https://simplevpn.gitlab.io/simplevpn-server',
    'repo_url': 'https://gitlab.com/simplevpn/simplevpn-server/',
    'repo_name': 'Source - GitLab',
    'repo_type': 'gitlab',
    'logo_icon': '<img src="_static/favicon.ico" width="32" />',
    'globaltoc_depth': 2,
    "heroes": {
        "index": "Create your own WireGuard-powered VPN Server with ease.",
        "installation": "Deploy it in minutes with Docker",
        "usage": "SimpleVPN User Guide",
        "customisation": "Customise SimpleVPN",
    },
}

html_show_sourcelink = False
html_sidebars = {
    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
}

# -- Extension configuration -------------------------------------------------

# -- Options for _todo extension ----------------------------------------------

# If true, `_todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True
