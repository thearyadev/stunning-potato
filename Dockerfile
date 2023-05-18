FROM python:3.11.3-slim-buster
ARG SERVICE

COPY . .

RUN pip install poetry==1.3.2
RUN poetry install

ENTRYPOINT "poetry run python launch.py --app ${SERVICE} --flush False"