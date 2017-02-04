#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from flask_mail import Mail
from config import config

db = SQLAlchemy()
csrf = CsrfProtect()
mail = Mail()


def create_app(config_name):
    print(config_name)
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
