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



NGINX config
------------
Create the file `/etc/nginx/sites-available/leq` and put this  in it:

```
upstream waiter_app_server {
  # fail_timeout=0 means we always retry an upstream even if it failed
  # to return a good HTTP response (in case the Unicorn master nukes a
  # single worker for timing out).

  server unix:/webapps/leq/run/gunicorn.sock fail_timeout=0;
}

upstream daphne_asgi_server {
  server unix:/webapps/leq/run/daphne.sock;
}

server {

    listen   80;
    server_name leq.sidewayspass.com;

    client_max_body_size 4G;

    access_log /webapps/leq/logs/nginx-access.log;
    error_log /webapps/leq/logs/nginx-error.log;

     location /static/ {
      alias   /webapps/leq/waiter/staticfiles/;
     }

    location / {
        # an HTTP header important enough to have its own Wikipedia entry:
        #   http://en.wikipedia.org/wiki/X-Forwarded-For
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # enable this if and only if you use HTTPS, this helps Rack
        # set the proper protocol for doing redirects:
        # proxy_set_header X-Forwarded-Proto https;

        # pass the Host: header from the client right along so redirects
        # can be set properly within the Rack application
        proxy_set_header Host $http_host;

        # we don't want nginx trying to do something clever with
        # redirects, we set the Host: header above already.
        proxy_redirect off;

        # set "proxy_buffering off" *only* for Rainbows! when doing
        # Comet/long-poll stuff.  It's also safe to set if you're
        # using only serving fast clients with Unicorn + nginx.
        # Otherwise you _want_ nginx to buffer responses to slow
        # clients, really.
        # proxy_buffering off;

        # Try to serve static files from nginx, no point in making an
        # *application* server like Unicorn/Rainbows! serve static files.
          proxy_pass http://waiter_app_server;
    }

    # Error pages
    error_page 500 502 503 504 /500.html;
    location = /500.html {
        root /webapps/leq/static/;
    }


    # via http://masnun.rocks/2016/11/02/deploying-django-channels-using-daphne/
    location ~ ^/(logs|progress|control)/ {
        proxy_pass http://daphne_asgi_server;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_redirect     off;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Host $server_name;
    }


}
```



