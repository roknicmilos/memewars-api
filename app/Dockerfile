FROM node:18.14 as base

COPY ./app/scripts                  /app/scripts
COPY ./scripts/colored_print.sh     /app/scripts/colored_print.sh
COPY ./app/src                      /app/src

WORKDIR /app/src

CMD ["sh", "/app/scripts/entrypoint.sh"]

########################
### PRODUCTION image ###
########################

FROM base AS production

ENV ENVIRONMENT='production'

RUN npm install -g serve

#########################
### STAGING image ###
#########################

FROM production AS staging

ENV ENVIRONMENT='staging'

#########################
### DEVELOPMENT image ###
#########################

FROM base AS development

ENV ENVIRONMENT='development'
