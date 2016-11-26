"""
This script runs the FlaskWebProject1 application using a development server.
"""

from os import environ
from src.server import app

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    httpd = make_server('localhost', 5555, app)
    httpd.serve_forever()
    HOST = environ.get('SERVER_HOST', 'localhost')

