FROM python:3.8
WORKDIR /temp/work_dir

# update pip
RUN python -m pip install --upgrade pip

# install packages
COPY requirements.txt /temp/work_dir
RUN pip install -r requirements.txt
COPY mirror_lg mirror_lg
COPY config config
# verify config file contains valid YAML)
RUN yamllint ./config/mlg_conf.yaml
COPY tests tests
COPY *.py ./
# run the tests, --skip-covered == ignore __init__.py files
RUN python -m coverage run --branch --source=mirror_lg -m unittest discover && \
    python -m coverage report --fail-under 67 -m --skip-covered
# execute linter
COPY pylintrc ./
RUN pylint --rcfile=pylintrc mlg_cli.py mirror_lg tests