Install
=========

This is where you write how to get a new laptop to run this project.


    virtualenv -p python3  venv
    source venv/bin/activate
    pip install -r requirements/local.txt
    
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py runserver
