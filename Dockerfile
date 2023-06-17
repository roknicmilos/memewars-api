FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y postgresql-client gettext

COPY --chmod=777    ./scripts/     /app/scripts/

COPY ./requirements     /app/requirements
COPY ./src              /app/src


RUN pip install --upgrade pip
RUN pip install -r /app/requirements/base.txt

WORKDIR /app/src

CMD ["sh", "/app/scripts/entrypoint.sh", "start"]
