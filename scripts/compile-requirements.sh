# Development
pip-compile \
    --extra dev \
    --extra check \
    --extra test \
    --extra doc \
    --extra notebook \
    --extra profile \
    --extra viz \
    --output-file="requirements/requirements.txt" \
    --resolver=backtracking \
    --quiet \
    "pyproject.toml"

# CI
pip-compile \
    --extra check \
    --extra test \
    --output-file="requirements/ci-requirements.txt" \
    --resolver=backtracking \
    --quiet \
    "pyproject.toml"
