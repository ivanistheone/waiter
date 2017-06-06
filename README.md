s/waiter/sushibar/g
===================

A test project for exploring Django channels as messaging layer for dashboard project.


Settings
--------

Use `config/settings/local.py` for local development (default option when running `./manage.py`).



Docker provision for dev and testing
------------------------------------
Create docker container images

    docker-compose build
    docker-compose up


Localhost provision
-------------------
You'll need thse on your localhost:

    postgres
    python3 


Install
-------

Code:
    virtualenv -p python3  venv
    source venv/bin/activate
    pip install -r requirements/local.txt
    npm install
    ./manage.py makemigrations

DB:
    createdb waiter
    ./manage.py migrate

For convenience there you can load an predefined admin user fixture using

    ./manage.py loaddata waiter/users/fixtures/admin_user.json

Then you can login with username `admin` and password `admin123`.
Alternatively, you can create a new admin account using:

    ./manage.py createsuperuser



Run in development
------------------

    ./manage.py runserver



Clean-slate restart
-------------------
This will drop all the data in the DB and restart:

    dropdb waiter
    createdb waiter
    rm -rf runs/migrations/0*.py
    ./manage.py makemigrations
    ./manage.py migrate
    ./manage.py loaddata waiter/users/fixtures/admin_user.json


Test coverage
-------------

To run the tests, check your test coverage, and generate an HTML coverage report::

    coverage run manage.py test
    coverage html
    open htmlcov/index.html


Running tests
-------------

    ./manage.py test runs



Live reloading and Sass CSS compilation
---------------------------------------

    gulp

see `gulpfile.js` for details.



Production deployment
---------------------

Use the `productoin.yml` docker file.
See [here](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html) for more info.
