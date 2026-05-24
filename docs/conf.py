"""
Configuration for the documentation generation.

"""

import sys
from importlib import metadata


project = 'wakeonlan'
version = metadata.version(project)
release = version
copyright = '2012, Remco Haszing'


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
]

intersphinx_mapping = {
    'python': (
        f'https://docs.python.org/{sys.version_info.major}.{sys.version_info.minor}',
        None,
    ),
}

nitpick_ignore = [('py:class', 'socket.AddressFamily')]

nitpicky = True

default_role = 'any'
todo_include_todos = True

master_doc = 'index'
html_theme = 'sphinx_rtd_theme'
