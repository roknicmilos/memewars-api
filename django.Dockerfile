FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_ROOT_DIR /app

RUN apt-get update && apt-get install -y postgresql-client gettext

# Create a user app without sudo permissions
RUN addgroup --gid 1000 app && adduser --uid 1000 --ingroup app --system app
RUN mkdir $APP_ROOT_DIR && chown app:app $APP_ROOT_DIR /var/log

USER app

COPY --chown=app:app . $APP_ROOT_DIR

RUN pip install --upgrade pip
RUN pip install -r $APP_ROOT_DIR/requirements/development.txt

WORKDIR $APP_ROOT_DIR

EXPOSE 8000
