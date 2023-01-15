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

   For older versions of Docker Compose use: `docker-compose up`


#### API

If the project is running, the API documentation should be available at
[api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)
and [api/schema/redoc/](http://localhost:8000/api/schema/redoc/).


### Tests and linting


#### Run tests

    docker exec -t meme-wars-django sh -c 'pytest'

The above command will run all tests. 
Flag `-t` is optional (it provides additional output coloring when used). 

To run the same tests in parallel, append `-n auto` to the `pytest` command:

    docker exec -t meme-wars-django sh -c 'pytest -n auto'

#### Run tests with coverage 
    
    docker exec meme-wars-django sh -c 'pytest --cov -n auto'    

This will run all tests in parallel with coverage report. 
Running tests like this is necessary to generate the tests coverage report.

#### Generate tests coverage report

    docker exec meme-wars-django sh -c 'coverage html'

This will generate html for the tests coverage report which is useful when trying 
to find out exactly which code is not covered by tests.
You can simply open the generated `index.html` in your browser and explore all files
and places in those files which are covered, not covered and ignored by tests coverage.

If you don't want the html, and you just want to see the overall coverage report, you
can run:

    docker exec meme-wars-django sh -c 'coverage report'

This will print the coverage report generated the last time tests wer run with the 
coverage ([Run tests with coverage](#run-tests-with-coverage)).

#### Run linter

    docker exec meme-wars-django sh -c 'flake8'

If there are no linting errors, the command will not have any output.
If there are linting errors, the output of the command will be those errors.

#### Simultaneously run tests, coverage and linter

    docker exec -t meme-wars-django sh -c '/app/scripts/check_project.sh'

The above command will run the `check_project.sh` script which will:
1. run all tests with coverage in parallel 
2. generate html for the coverage report 
3. run the linter

The flag `-t` is optional just like when [only running tests](#run-tests).


### Initial Data

#### Create a superuser

Superuser should already be created after running `docker compose up`
with the credentials from `.env` file. If you want to create a new one, run:

    docker exec -t meme-wars-django sh -c 'python3 manage.py create_superuser'

If the superuser with the credentials from the `.env` file does not exist, you 
can create it by running: 

    docker exec meme-wars-django sh -c 'python3 manage.py create_superuser --noinput'

#### Load fixtures

To load all the fixtures, run the comment below (**NOTE: this will override table
raws with the same primary keys as those specified in fixtures**):

    docker exec meme-wars-django sh -c 'python3 manage.py load_data'

Or you can load specific fixtures (in a specific order) by passing them as arguments to the same
command. For example, to load `users` fixtures, and then `wars` fixtures:

    docker exec meme-wars-django sh -c 'python3 manage.py load_data users wars'


## Production setup

Production setup requirements and steps are the same as for [Development setup](#development-setup), 
and the only thing that differs is that you have to specify a different Docker Compose file when 
starting the app:

    docker compose -f docker-compose.production.yml up

None of the [Initial data](#initial-data) will be loaded in this case, but you can load it manually.

