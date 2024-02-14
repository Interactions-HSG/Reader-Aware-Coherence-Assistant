# -*- coding: utf-8 -*-
# 
from flask_cors import CORS # This is generally important for online applications where you want your APIs to be accessible by other domains.
from flask import Flask, render_template, request, jsonify, send_from_directory
import requests as rq

from reader_profile import my_fetch

from . import metrics

app = Flask(__name__)
CORS(app)

#  the is the declaration of the flask app
__all__ = ['app',
    'my_fetch', 
    'CORS',
    'Flask', 'render_template', 'request', 'jsonify',
    'rq',
    'metrics'
]
