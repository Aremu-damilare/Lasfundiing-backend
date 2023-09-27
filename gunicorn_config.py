import multiprocessing

bind = "0.0.0.0:8080"
certfile = "/etc/ssl/certs/certificate.crt"
keyfile = "/etc/ssl/private/private.key"
workers = multiprocessing.cpu_count() * 2 + 1



