# qwerty

Table of Contents
=================

* [Development setup](#development-setup)
* [Production setup](#development-setup)


## Development setup

### Prerequisite

- [Python](https://www.python.org/downloads/)
- (**Optional**) [venv](https://docs.python.org/3/library/venv.html)

### Steps

1. (**Optional**) Setup virtual environment. If you want to start the project in
   virtual environment, and you installed [venv](https://docs.python.org/3/library/venv.html),
   follow the next steps to create and activate virtual environment:
    - Go into project root directory and create virtual environment:

      `python3 -m venv venv`

    - Activate virtual environment:

      `source venv/bin/activate` (Linux bash)

      **OR**

      `venv\Scripts\activate.bat` (Windows cmd)


2. Start server

   `python manage.py runserver`

   This will start a lightweight development server (that comes with Django)
   at http://127.0.0.1:8000/.


## Production setup

### Prerequisite

- [Python](https://www.python.org/downloads/)
- (**Optional**) [venv](https://docs.python.org/3/library/venv.html)

### Steps

1. (**Optional**) Setup virtual environment. If you want to start the project in
   virtual environment, and you installed [venv](https://docs.python.org/3/library/venv.html),
   follow the next steps to create and activate virtual environment:
    - Go into project root directory and create virtual environment:

      `python3 -m venv venv`

    - Activate virtual environment:

      `source venv/bin/activate` (Linux bash)

      **OR**

      `venv\Scripts\activate.bat` (Windows cmd)


3. Start server:

   `./start_gunicorn.sh`

   This will run migrations, collect static files and start Gunicorn production server at
   http://127.0.0.1:8000/. Check files in `run/logs/gunicorn/` directory for access and error 
   logs.
