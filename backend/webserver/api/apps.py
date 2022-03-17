from django.apps import AppConfig
from django.core.signals import request_started


class ApiConfig(AppConfig):
    name = 'api'
    verbose_name = 'AGVN API'

    def ready(self):
        request_started.connect(self.log_request)

    def log_request(self, sender, environ, **kwargs):
        host = environ['HTTP_HOST']
        path = environ['PATH_INFO']
        query = environ['QUERY_STRING']
        query = '?' + query if query else ''
        print(f"Request Received FROM {host}{path}{query}")
