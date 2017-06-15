import os

from fabric.api import *
from fabric.context_managers import shell_env

env.hosts = [
    '35.188.9.9',
]

def pull():
    env.user   = "leq"
    code_dir = '/webapp/waiter'
    with cd(code_dir):
        run("git pull")

def update():
    env.user   = "leq"
    code_dir = '/webapp/waiter'
    with cd(code_dir):
        with prefix("source sushibar/bin/activate"):
            run("git pull")
            run("pip install -r requirements/production.txt")
            run("./manage.py collectstatic --noinput")

def deploy():
    env.user = "bharadwajs"
    env.shell = "/bin/sh -c"
    sudo("supervisorctl restart leq", pty=False)
    sudo("supervisorctl restart leq_channels_workers", pty=False)
    sudo("supervisorctl restart leq_channels_daphne", pty=False)

