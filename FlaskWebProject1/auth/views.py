from flask import flash, render_template, redirect, url_for, request
from . import auth

"""
In case we want to save stuff on google drive
"""


@auth.route('/login', methods=['GET', 'POST'])
def login():
    pass


@auth.route('/logout')
def logout():
    pass
