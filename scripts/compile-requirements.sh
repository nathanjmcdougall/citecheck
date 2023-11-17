# Development
pip-compile \
    --extra dev \
    --extra check \
    --extra test \
    --extra doc \
    --extra notebook \
    --extra profile \
    --extra viz \
    --no-allow-unsafe \
    --unsafe-package=pywin32 \
    --unsafe-package=pip \
    --unsafe-package=distribute \
    --unsafe-package=setuptools \
    --output-file="requirements/requirements.txt" \
    --resolver=backtracking \
    --quiet \
    "pyproject.toml"

# CI
pip-compile \
    --extra check \
    --extra test \
    --no-allow-unsafe \
    --unsafe-package=pywin32 \
    --unsafe-package=pip \
    --unsafe-package=distribute \
    --unsafe-package=setuptools \
    --output-file="requirements/ci-requirements.txt" \
    --resolver=backtracking \
    --quiet \
    "pyproject.toml"
