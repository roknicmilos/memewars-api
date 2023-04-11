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
RUN pip install -r /app/requirements/base.txt

WORKDIR /app/src

CMD ["sh", "/app/scripts/entrypoint.sh"]

########################
### PRODUCTION image ###
########################

FROM base AS production

ENV ENVIRONMENT='production'

########################
### STAGING image ###
########################

FROM base AS staging

ENV ENVIRONMENT='staging'

#########################
### DEVELOPMENT image ###
#########################

FROM base AS development

ENV ENVIRONMENT='development'
