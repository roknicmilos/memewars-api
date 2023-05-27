# meme wars

Table of Contents
=================

* [Project setup](#project-setup)
    * [Requirements](#requirements)
    * [Steps](#steps)
* [Tests and linting](#tests-and-linting)
* [Initial data](#initial-data)
* [Updating dependencies](#updating-dependencies)

## Project setup

### Requirements

- **Docker**:
    - Windows - [Docker Desktop for Windows](https://docs.docker.com/docker-for-windows/install/)
    - Mac - [Docker Desktop for Mac](https://docs.docker.com/docker-for-mac/install/)
    - Linux - [Docker Engine](https://docs.docker.com/engine/install/#server)
      and [Docker Compose](https://docs.docker.com/compose/install/)

### Steps

1. Create `.env` based on `example.env`
2. Start the app: `docker compose up`

   For older versions of Docker Compose use: `docker-compose up`

**NOTE**: There are multiple `docker exec` command in the text that follows. 
This command is executed for a running container, which means that everywhere 
this command is mentioned, we assume that the container for which this command 
is being executed is running. 
Check if containers are running with `docker ps` command.
Also, we assume that container suffix is not defined (`CONTAINERS_SUFFIX` 
environment variable) and use original container name (without suffix) throughout
this entire document.
You can use `docker ps` to list all running containers and their full names.

## Tests and linting

### Run tests

    docker exec -t memewars-django sh -c 'pytest'

The above command will run all tests.
Flag `-t` is optional (it provides additional output coloring when used).

To run the same tests in parallel, append `-n auto` to the `pytest` command:

    docker exec -t memewars-django sh -c 'pytest -n auto'

### Run tests with coverage

    docker exec -t memewars-django sh -c 'pytest --cov -n auto'    

This will run all tests in parallel with coverage report.
Running tests like this is necessary to generate the tests coverage report.

### Generate tests coverage report

    docker exec memewars-django sh -c 'coverage html'

This will generate html for the tests coverage report which is useful when trying
to find out exactly which code is not covered by tests.
You can simply open the generated `index.html` in your browser and explore all files
and places in those files which are covered, not covered and ignored by tests coverage.

If you don't want the html, and you just want to see the overall coverage report, you
can run:

    docker exec memewars-django sh -c 'coverage report'

This will print the coverage report generated the last time tests wer run with the
coverage ([Run tests with coverage](#run-tests-with-coverage)).

### Run linters

- **Code security**:

        docker exec memewars-django sh -c 'bandit .'

  The above command will run [Bandit](https://bandit.readthedocs.io/) will check for
  security issues in Python code.


- **Code quality**:

        docker exec memewars-django sh -c 'flake8'

  The above command will run [Flake8](https://flake8.pycqa.org/) runs multiple tools to
  check the quality of Python code.
  If there are no issues, the command will not have any output.
  If there are issues, they will be displayed in the output of the command.

### Simultaneously run tests, coverage and linters

    docker exec -t memewars-django sh -c '/app/scripts/check_project.sh'

The above command will run the `check_project.sh` script which will:

1. run all tests with coverage in parallel
2. generate html for the coverage report
3. run [Bandit](https://bandit.readthedocs.io/) to check security of Python code
4. run [Flake8](https://flake8.pycqa.org/) to check quality of Python code

The flag `-t` is optional just like when [only running tests](#run-tests).

## Initial Data

### Create a superuser

Superuser should already be created after running `docker compose up`
with the credentials from `.env` file. If you want to create a new one, run:

    docker exec -t memewars-django sh -c 'python3 manage.py createsuperuser'

If the superuser with the credentials from the `.env` file does not exist, you
can create it by running:

    docker exec memewars-django sh -c 'python3 manage.py createsuperuser --noinput'

### Load fixtures

To load all the fixtures, run the comment below (**NOTE: this will override table
raws with the same primary keys as those specified in fixtures**):

    docker exec memewars-django sh -c 'python3 manage.py load_data'

Or you can load specific fixtures (in a specific order) by passing them as arguments to the same
command. For example, to load `users` fixtures, and then `wars` fixtures:

    docker exec memewars-django sh -c 'python3 manage.py load_data users wars'

## Updating dependencies

Execute the following set of commands to interactively upgrade requirements packages:

    docker compose exec django bash -c 'pip install pip-upgrader && 
        pip-upgrade /app/requirements/*.txt --skip-virtualenv-check --skip-package-installation'
