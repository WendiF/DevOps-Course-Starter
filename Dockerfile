FROM python:3.9-slim-buster as base
WORKDIR /todo_app
RUN pip3 install poetry
COPY poetry.lock pyproject.toml wsgi.py ./
RUN poetry config virtualenvs.create false
# production build stage
FROM base as production
COPY todo_app ./todo_app
RUN poetry install --no-dev
ENTRYPOINT ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:80", "wsgi:run()"]
# local development stage
FROM base as development
RUN poetry install
ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]