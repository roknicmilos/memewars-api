FROM node:18.14

COPY ./src      /app/src
COPY ./scripts  /app/scripts

WORKDIR /app/src

CMD ["sh", "/app/scripts/entrypoint.sh"]
