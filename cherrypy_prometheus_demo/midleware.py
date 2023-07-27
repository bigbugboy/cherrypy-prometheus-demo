import socket

import cherrypy
from prometheus_client import Counter, Histogram


class PrometheusMiddleware:

    ApiRequestCounter = Counter(
        'http_request_url_counter',
        'different url req counter',
        labelnames=['hostname', 'method', 'endpoint', 'status'],
    )
    ApiResponseTimeHis = Histogram(
        'http_response_seconds',
        'http response time',
        labelnames=['hostname', 'method', 'endpoint'],
    )
    HOST_NAME = socket.gethostname()

    def __init__(self, nextapp):
        self.nextapp = nextapp

    def __call__(self, environ, start_response):
        method = environ.get('REQUEST_METHOD')
        endpoint = environ.get('REQUEST_URI', '').split('?')[0]
        host_name = self.HOST_NAME

        with self.ApiResponseTimeHis.labels(host_name, method, endpoint).time():
            res = self.nextapp(environ, start_response)

        status = cherrypy.response.status.split()[0]
        self.ApiRequestCounter.labels(host_name, method, endpoint, status).inc()
        return res
