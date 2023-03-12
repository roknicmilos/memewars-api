FROM python:3.11 as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y postgresql-client gettext

COPY ./api/scripts                /app/scripts
COPY ./scripts/colored_print.sh   /app/scripts/colored_print.sh
RUN chmod -R 775                  /app/scripts

COPY ./api/requirements     /app/requirements
COPY ./api/src              /app/src


RUN pip install --upgrade pip

WORKDIR /app/src

CMD ["sh", "/app/scripts/entrypoint.sh"]

########################
### PRODUCTION image ###
########################

FROM base AS production

ENV ENVIRONMENT='production'

RUN pip install -r /app/requirements/production.txt

########################
### STAGING image ###
########################

FROM production AS staging

ENV ENVIRONMENT='staging'

#########################
### DEVELOPMENT image ###
#########################

FROM base AS development

ENV ENVIRONMENT='development'

RUN pip install -r /app/requirements/development.txt
