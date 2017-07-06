s/waiter/sushibar/g
===================

A test project for exploring Django channels as messaging layer for dashboard project.


Settings
--------
  - Use `config/settings/base.py` for common settings
  - Use `config/settings/local.py` for local development settings (default option when running `./manage.py`).
  - Use `config/settings/production.py` for added prod security restrictions.
    Credentials will be `source`d from the file `.prodenv`.



Localhost provision
-------------------
You'll need to install Postgres DB and Python3 on your machine.


Docker provision for dev and testing
------------------------------------
Create docker container images

    docker-compose build
    docker-compose up



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


Live reloading and Sass CSS compilation
---------------------------------------

    gulp

see `gulpfile.js` for details.


Running tests
-------------

    ./manage.py test runs



Clean-slate restart
-------------------
This will drop all the data in the DB and restart:

    dropdb waiter
    createdb waiter
    rm -rf runs/migrations/0*.py
    ./manage.py makemigrations
    ./manage.py migrate
    ./manage.py loaddata waiter/users/fixtures/admin_user.json




Docker production deployment
----------------------------
Use the `production.yml` docker file. **(Currently not supported)**


