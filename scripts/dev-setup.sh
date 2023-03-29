PYTHON_VERSION=$(cat .python-version | sed 's/\r//') &&
pyenv install $PYTHON_VERSION -s &&
pyenv shell $PYTHON_VERSION &&
python -m venv .venv &&
source .venv/bin/activate &&
python -m ensurepip &&
python -m pip install --upgrade pip &&
pip install pip-tools &&
pip-sync requirements.txt &&
pre-commit install
