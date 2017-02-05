#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request, jsonify

from . import main


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


