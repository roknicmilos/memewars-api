# meme wars


## Development setup

### Setup requirements

- **Docker**:
    - Windows - [Docker Desktop for Windows](https://docs.docker.com/docker-for-windows/install/)
    - Mac - [Docker Desktop for Mac](https://docs.docker.com/docker-for-mac/install/)
    - Linux - [Docker Engine](https://docs.docker.com/engine/install/#server)
      and [Docker Compose](https://docs.docker.com/compose/install/)

### Setup steps

1. Create `.env` based on `example.env`
2. Start the app: `docker compose up`

   (for older versions of Docker Compose use: `docker-compose up`)

### Initial Data

#### Create a superuser

Superuser should already be created after running `docker compose up`
with the credentials from `.env` file. If you want to create a new one, run:

    `docker exec -it meme-wars-django sh -c 'python manage.py create_superuser'`

If the superuser with the credentials from the `.env` file does not exist, you 
can create it using the above command with `--noinput`. 

#### Load fixtures

To load the fixtures, run the comment below (**NOTE: this will override table
raws with the same primary keys as those specified in fixtures**):

    `docker exec -it meme-wars-django sh -c 'python manage.py load_data'`


## Production setup

Production setup requirements and steps are the same as for [Development setup](#development-setup), 
and the only thing that differs is that you have to specify a different Docker Compose file when 
starting the app:

    `docker compose -f docker-compose.production.yml up`

None of the [Initial data](#initial-data) will be loaded in this case, but you can load it manually.

