"""Configuration file for the Sphinx documentation builder."""

from pathlib import Path

import tomli

# Sphinx expects some non-pylint compliant names
# pylint: disable=invalid-name
ROOT_PATH = Path(__file__).parent.parent.parent

with open(ROOT_PATH / "pyproject.toml", mode="rb") as f:
    _pyproject = tomli.load(f)

_project = _pyproject["project"]
_name = _project["name"]
_authors = _project["authors"]
_first_author = _authors[0]["name"]
_description = _project["description"]
language = "en"
source_suffix = [".rst"]
source_encoding = "utf-8"


extensions = [
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_toggleprompt",
    "sphinx_favicon",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.ifconfig",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
]

name = _name
author = _first_author
description = _description

templates_path = ["_templates"]
exclude_patterns = []

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

napoleon_google_docstring = True

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_theme_options = {
    "github_url": "https://github.com/nathanjmcdougall/citecheck",
    "pygment_light_style": "tango",
    "pygment_dark_style": "monokai",
    "logo": {
        "image_light": "logo-light.png",
        "image_dark": "logo-dark.png",
        "alt_text": "Documentation - Index",
    },
}
favicons = [{"href": "favicon.ico"}]


def linkcode_resolve(domain, info):
    """Determine the URL corresponding to Python object."""
    if domain != "py":
        return None
    if not info["module"]:
        return None
    filename = info["module"].replace(".", "/")
    return f"https://github.com/nathanjmcdougall/citecheck/{filename}.py"
