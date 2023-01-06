FROM python:3.11 as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y postgresql-client gettext

COPY ./scripts  /app/scripts
RUN chmod -R 775  /app/scripts

COPY ./requirements     /app/requirements
COPY ./src              /app/src


RUN pip install --upgrade pip

WORKDIR /app/src

ENTRYPOINT ["sh", "/app/scripts/entrypoint.sh"]

########################
### PRODUCTION image ###
########################

FROM base AS production

ENV APP_ENV='production'

RUN pip install -r /app/requirements/production.txt

#########################
### DEVELOPMENT image ###
#########################

FROM base AS development

ENV APP_ENV='development'

RUN pip install -r /app/requirements/development.txt
