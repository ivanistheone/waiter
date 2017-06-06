from fabric.api import *
from fabric.context_managers import shell_env

env.hosts = [
    'leq.sidewayspass.com',
]

def pull():
    env.user   = "leq"
    code_dir = '/webapps/leq/waiter'
    with cd(code_dir):
      run("git pull")

def update():
    env.user   = "leq"
    code_dir = '/webapps/leq/waiter'
    with cd(code_dir):
      with prefix("source activate"):
        run("git pull")
        run("pip install -r requirements/production.txt")

def deploy():
  env.user = "arvnd"
  env.shell = "/bin/sh -c"
  sudo("supervisorctl restart leq", pty=False)