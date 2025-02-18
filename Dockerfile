FROM python:3.12.8-bullseye

COPY dana_data_quality /
COPY poetry.lock /
COPY pyproject.toml / 

RUN curl -sSL https://install.python-poetry.org | python3 -
RUN /root/.local/bin/poetry config virtualenvs.create false
RUN /root/.local/bin/poetry install
