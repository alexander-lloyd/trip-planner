#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from .filters import to_pounds, to_plural

main = Blueprint('main', __name__)

main.add_app_template_filter(to_pounds, 'toPounds')
main.add_app_template_filter(to_plural, 'toPlural')

from . import views
