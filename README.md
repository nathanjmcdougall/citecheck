<h1 align="center">
  <img src="doc/source/_static/logo/full_dark.svg#gh-dark-mode-only"><br>
  <img src="doc/source/_static/logo/full_light.svg#gh-light-mode-only"><br>
</h1>

# citecheck: like typechecks, but for citations 📖⛓️

<!-- badges: start -->
[![License](https://img.shields.io/github/license/nathanjmcdougall/citecheck)](https://github.com/nathanjmcdougall/citecheck/blob/main/LICENSE.txt)
[![PyPI version](https://badge.fury.io/py/citecheck.svg)](https://badge.fury.io/py/citecheck)
[![Documentation Status](https://readthedocs.org/projects/citecheck/badge/?version=latest)](https://citecheck.readthedocs.io/en/latest/?badge=latest)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Linting: Ruff](https://img.shields.io/badge/linting-ruff-yellowgreen)](https://github.com/charliermarsh/ruff)
[![Linting: Pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/nathanjmcdougall/citecheck/main.svg)](https://results.pre-commit.ci/latest/github/nathanjmcdougall/citecheck/main)
[![codecov](https://codecov.io/gh/nathanjmcdougall/citecheck/branch/develop/graph/badge.svg?token=OUHWT2NL8O)](https://codecov.io/gh/nathanjmcdougall/citecheck)
[![Downloads](https://static.pepy.tech/badge/citecheck)](https://pepy.tech/project/citecheck)
<!-- badges: end -->

## Quick example

Consider this example (all authors and quantities are fictitious):

- Doe (2021) published a method for estimating $V_t$ as a function of $q_p$ and $t$.
- Bloggs (2023) published a method for estimating $R_m$ as a function of $V_t$ and
  $\rho$, with the explicit requirement that $V_t$ be estimated using the method of
  Doe (2021) in particular.

The goal for citecheck is that you could implement this as follows:

```Python
from citecheck import enforcecite, Cite

@enforcecite
def calc_vt_doe2021(
  qt: float,
  t: float
) -> Annotated[float, Cite("doe2021")]:
    ...

@enforcecite
def calc_rm_bloggs2023(
  vt: Annotated[float, Cite("doe2021")],
  rho: float
) -> Annotated[float, Cite("bloggs2023")]:
    ...
```

Now, if we try to pass a value for $V_t$ that was not estimated using the method of Doe
(2021), we would get an error:

```Python
calc_rm_bloggs2023(vt=1.0, rho=1.0) # Error
calc_rm_bloggs2023(vt=calc_vt_doe2021(1.0, 1.0), rho=1.0) # OK
```

citecheck is still in development, but this is the general idea.

## When to use citecheck

You should consider using citecheck when you are implementing functions corresponding to
equations or methodologies in multiple papers which refer to one another.

## Getting Started with Development

Use Linux, install [`pyenv`](https://github.com/pyenv/pyenv), and then run the setup
script:

```bash
source .\scripts\dev-setup.sh
```
