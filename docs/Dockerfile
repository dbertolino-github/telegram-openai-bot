FROM python:3.10

# Sphinx
RUN apt-get update && apt-get install -y build-essential
RUN pip install --upgrade pip && pip install sphinx sphinx-rtd-theme sphinx-serve myst_parser

WORKDIR /code/docs

# CODE Backend
ADD src/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

## ER diagram
RUN apt-get update && apt-get install -y graphviz graphviz-dev
RUN pip install pygraphviz pydot

CMD sphinx-serve --build build --port 8081 --host 0.0.0.0