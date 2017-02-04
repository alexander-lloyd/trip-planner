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


@main.route('/data/autocomplete')
def autocomplete():
    """

    :return: Json in the form:

    {
    "suggestions": [ "United Arab Emirates", "United Kingdom", "United States" ]
    }

    """
    query = request.args.get('term', '')
    if query != '':
        return jsonify({
            "suggestions": ["United Arab Emirates", "United Kingdom", "United States"]
        })
