# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

import sphinx_rtd_theme


# -- Path setup --------------------------------------------------------------

sys.path.insert(0, os.path.abspath('../'))


# -- Project information -----------------------------------------------------

project = 'inept'
copyright = '2021, inept development team'
author = 'inept development team'

# The full version, including alpha/beta/rc tags
try:
    from inept import __version__ as release
except:
    release = None


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'nbsphinx',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']
html_static_path = []


# -- setup() -----------------------------------------------------------------

def run_apidoc(_):
    from sphinx.ext.apidoc import main
    import os
    import shutil
    cur_dir = os.path.dirname(__file__)
    module = os.path.join(cur_dir, '../../inept')
    output_path = os.path.join(cur_dir, 'api')
    shutil.rmtree(output_path, ignore_errors=True)
    main(['--separate',
        '--module-first',
        '--no-toc',
        '--force',
        '-o', output_path, module,
    ])


def setup(app):
    app.connect('builder-inited', run_apidoc)
