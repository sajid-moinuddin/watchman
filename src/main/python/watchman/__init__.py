from __future__ import absolute_import

VERSION = '${version}'


def decode1364(encoded_string):
    return encoded_string.decode('rot13').decode('base64')


def initialize_logging():
    pass
