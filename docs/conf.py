"""
Configuration for the documentation generation.

"""
import pkg_resources


project = 'wakeonlan'
_dist = pkg_resources.get_distribution(project)

version = _dist.version
release = _dist.version
copyright = '2012, Remco Haszing'


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3.11', None),
}

nitpick_ignore = [('py:class', 'socket.AddressFamily')]

nitpicky = True

default_role = 'any'
todo_include_todos = True

master_doc = 'index'
html_theme = 'sphinx_rtd_theme'
