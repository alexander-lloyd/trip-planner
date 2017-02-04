#!/usr/bin/env python
# -*- coding: utf-8 -*-


def to_pounds(value):
    return '£{:.2f}'.format(value)


def to_plural(value, singular, plural):
    if value == 1:
        return '{} {}'.format(value, singular)
    else:
        return '{} {}'.format(value, plural)