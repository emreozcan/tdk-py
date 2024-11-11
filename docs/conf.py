import dunamai

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'tdk-py'
copyright = '2024, Emre Özcan'
author = 'Emre Özcan'
release = dunamai.Version.from_git().serialize()

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.autodoc',
    'myst_parser',
    'sphinx_copybutton',
    'autodoc2',
    'sphinx_inline_tabs',
    'sphinx_tippy',
]

templates_path = ['_templates']
exclude_patterns = []

# -- MystParser

myst_enable_extensions = [
    'attrs_block',
    'colon_fence',
    'fieldlist',
]
myst_heading_anchors = 3

# -- Internationalization
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-gettext_uuid

gettext_uuid = True
gettext_compact = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

# -- Options for autodoc2

autodoc2_packages = [
    '../src/tdk',
]
autodoc2_render_plugin = "myst"
autodoc2_module_all_regexes = [
    # r'tdk\..*',
]
autodoc2_hidden_objects = {"inherited", "private"}
autodoc2_replace_annotations = [
    ("tdk.etc.tools._T", "T"),
]

# -- Options for intersphinx
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pydantic': ('https://docs.pydantic.dev/2.9', None),
    'aiohttp': ('https://docs.aiohttp.org/en/v3.10.10/', None),
}
