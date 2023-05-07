FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y postgresql-client gettext

COPY ./api/scripts                /app/scripts
COPY ./scripts/utils.sh   /app/scripts/utils.sh
RUN chmod -R 775                  /app/scripts

COPY ./api/requirements     /app/requirements
COPY ./api/src              /app/src


RUN pip install --upgrade pip
RUN pip install -r /app/requirements/base.txt

WORKDIR /app/src

CMD ["sh", "/app/scripts/entrypoint.sh"]
