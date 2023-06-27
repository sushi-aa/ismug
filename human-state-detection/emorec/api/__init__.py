from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import json

from werkzeug.serving import make_server

from service import ServiceThread

db = SQLAlchemy()

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config')

app.config.from_pyfile('config.py')
app.config.from_file('config/hw.json', load=json.load)
app.config.from_file('config/emotions.json', load=json.load)

db.init_app(app)

from . import views

class WebAPI(ServiceThread):
    def __init__(self, host, port, app):
        super().__init__()
        self._srv = make_server(host, port, app)
        self._ctx = app.app_context()
        self._ctx.push()
    
    def run(self):
        self._srv.serve_forever()
    
    def stop(self):
        self._srv.shutdown()
        super().stop()
