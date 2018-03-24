"""
Configuration for the documentation generation.

"""
import pkg_resources


project = 'wakeonlan'
_dist = pkg_resources.get_distribution(project)

version = _dist.parsed_version.base_version
release = _dist.version
copyright = '2012, Remco Haszing'


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3.6', None),
}

nitpicky = True

default_role = 'any'
todo_include_todos = True

master_doc = 'index'
html_theme = 'sphinx_rtd_theme'
