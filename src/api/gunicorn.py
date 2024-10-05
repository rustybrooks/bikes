import logging.config

workers = 4
# accesslog = "/srv/logs/gunicorn_access.log"
# errorlog = " /srv/logs/gunicorn_errors.log"
preload_app = True
# worker_class = 'gevent'
worker_class = "gthread"
threads = 4
timeout = 200

# max_requests = 10000
# max_requests_jitter = int(max_requests / 2)
