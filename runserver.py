"""
This script runs the FlaskWebProject1 application using a development server.
"""

from os import environ
from FlaskWebProject1 import create_app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    CONFIG = environ.get('FLASK_CONFIG', 'default')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app = create_app(CONFIG)
    app.run(HOST, PORT)
