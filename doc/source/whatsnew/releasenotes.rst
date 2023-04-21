0.2.0 (2023-04-21)
==================

Features
--------

- Mypy has been added to the project for static type checking, in strict mode.
  Accordingly, comprehensive type annotations have been added to the codebase, excluding
  the test suite. (#40)
- A decorator ``check_citations`` has been added, which together with a class ``Cite`` and
  ``typing.Annotated`` automate's the checking of citation arguments to a function. (#71)
- The decorator ``check_citations`` has new behaviour to use ``typing.Annotated``
  together with a instance of the container class ``Cite``, rather than ``CiteAs``
  directly. (#82)
- An as-yet-unused square logo has been designed and added to the ./doc
  folder. It is intended to be used as a favicon for the documentation website, but as yet
  has not been configured to be used for that purpose. Full sized logos have also been
  added, as used in the README.
- Most parts of the core functionality have now been implemented, but also changed
  significantly; especially ``CiteAs`` and its dependents.


Improved Documentation
----------------------

- pyproject.toml has been configured with pakcage metadata for in PyPI. This includes
  classifiers, project URLs, and the SPDX license identifier. (#5)
- Badges in the README have been added and re-ordered. Also, one for the Python version
  used in development has been removed. (#43)
- The README has been improved to include a logo (dark and light mode adaptive), a
  slogan, a quick example, basic guidance on when to use the package, and explicit
  reference to pyenv usage.
- The changelog entry for v0.1.2 was incorrectly headered as v0.1.1. This used single
  backticks for the code blocks, whereas these should be double backticks in RST.
  Both these issues have been addressed.


Renamings and Relocations
-------------------------

- ``Citand`` has been renamed to ``Citable``. The original name was a nod to the words
  multiplicand and summand. (#12)


Improved Test Suite
-------------------

- New tests have been added, corresponding to the re-designed core classes.


Development Configuration Changes
---------------------------------

- Dependabot has been configured to work correctly when using pip-compile together with
  pyproject.toml. To achieve this, the CI requirements.txt file was renamed from
  requirements-ci.txt to ci-requirements.txt, to follow dependabot's expected naming
  pattern for requiremnts files. An empty requirements.in file also needed to be added
  to signal to dependabot that pip-compile is being used. (#4)
- The requirements.txt files (for local development and CI) have been put into a
  subdirectory to reduce clutter. (#61)
- A CI check has been added to ensure the requirements.txt for local development is
  coherent via a dry-run pip install.
- Codecov has been configured to analyze code coverage of the repository.
- Custom towncrier fragment types have been added. These are: feature, bugfix, doc,
  removal, newhome, test, and config.
- Dependabot updates are now scheduled for daily, rather than weekly.
- Some non-printable characters have been removed from many files, especially carriage
  returns. Some tools were not able to work properly with these characters.
- The ``citecheck[dev,check]`` extras now use fixed versions of various utilities shared
  in common with pre-commit, rather than leaving this to pip-compile. When dependabot
  updates these, the pre-commit config file needs to be manually updated to match the
  suggested new versions.
- The license file is now specified to setuptools in pyproject.toml.
- The pylint message useless-object-inheritance is now disabled since for mypy, explicit
  inheritance from object is useful.


0.1.2 (2023-03-30)
==================

Features
--------

- Added core functionality, including ``CiteAs``, ``Cited``, and ``check_citations``.
