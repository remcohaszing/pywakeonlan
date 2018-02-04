"""
Configuration for the documentation generation.

"""
project = 'Python wakeonlan'

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
