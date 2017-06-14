Production setup
================


Overview
--------
For the Django HTTP application we use:

  - `configs/wsgi.py` and `config/settings/production.py`
  - Environment variables in startup script

For the channels/WebSocket stuff, we use:

  - `configs/asgi.py` + `runs/routing.py` + `runs/ws_logs.py`
  - and the production config `config/settings/production.py`



Scripts
-------
For the current setup on [leq.sidewayspass.com](http://leq.sidewayspass.com/)
we're using a python virtualenv which requires custom startup scripts.
These are currently not comitted to the source repo but you can find them on the
server in the `/webapps/leq/waiter/bar/bin`

The three scripts are `gunicorn_start` (for starting WSGI application),
and `daphne_start` plus `worker_start` for all the ASGI stuff.

In the final setup we'll use the system python repositories so these scripts
won't be necessary anymore: we'll be able to do all the setup using the supervisor config.




Supervisor config
-----------------

Create the file `/etc/supervisor/conf.d/leq.conf`

```
[program:leq]
command = /webapps/leq/waiter/bar/bin/gunicorn_start                    ; Command to start app
user = leq
stdout_logfile = /webapps/leq/logs/gunicorn_supervisor.log   ; Where to write log messages
redirect_stderr = true                                                ; Save stderr in the same log
environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8


[program:leq_channels_daphne]
command = /webapps/leq/waiter/bar/bin/daphne_start                    ; Command to start app
user = leq
stdout_logfile = /webapps/leq/logs/leq_channels_daphne.log
redirect_stderr = true


[program:leq_channels_workers]
command = /webapps/leq/waiter/bar/bin/worker_start                    ; Command to start app
user = leq
stdout_logfile = /webapps/leq/logs/leq_channels_workers.log
redirect_stderr = true
```

Then run

    supervisorctl reread
    supervisorctl reload

    supervisorctl status




