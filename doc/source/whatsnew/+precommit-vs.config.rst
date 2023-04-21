The ``citecheck[dev,check]`` extras now use fixed versions of various utilities shared
in common with pre-commit, rather than leaving this to pip-compile. When dependabot
updates these, the pre-commit config file needs to be manually updated to match the
suggested new versions.
