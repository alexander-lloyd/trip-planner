#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "KHFLKJADSFHLSDJKFHLKJDNKJLhldkjghdsjklfnlkjh@:l(*&(*&^&%&*^"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

    MAIL_SERVER = 'smtp-mail.outlook.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'trip-planner@outlook.com'
    MAIL_PASSWORD = 'l@w3wq%GrW'
    MAIL_DEFAULT_SENDER = 'Development Team!'
    MAIL_SUBJECT_PREFIX = '[Trip Planner] '


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + \
                                                                    os.path.join(basedir, 'database-dev.db')
    SQLALCHEMY_RECORD_QUERIES = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + \
                                                                os.path.join(basedir, 'database.db')

    @classmethod
    def init_app(cls, app):
        return
        Config.init_app(app)

        # email all errors to admins (me)
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.APP_MAIL_SENDER,
            toaddrs=[cls.APP_ADMIN],
            subject=cls.APP_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class HerokuConfig(ProductionConfig):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        from werkzeug.contrib.fixers import ProxyFix  # TODO: Do I need this?
        app.wsgi_app = ProxyFix(app.wsgi_app)

        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


class AzureConfig(ProductionConfig):
    pass


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': AzureConfig,
    'azure': AzureConfig
}
