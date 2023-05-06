FROM node:18.14

COPY ./app/scripts                  /app/scripts
COPY ./scripts/utils.sh     /app/scripts/utils.sh
COPY ./app/src                      /app/src

WORKDIR /app/src

CMD ["sh", "/app/scripts/entrypoint.sh"]
