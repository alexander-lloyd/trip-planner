from flask import flash, render_template, redirect, url_for, request
from . import auth


@auth.context_processor
def auth_add_template_variables():
    return {}


@auth.before_request
def auth_before_request():
    pass


@auth.route('/login', methods=['GET', 'POST'])
def login():
    pass


@auth.route('/logout')
def logout():
    pass
