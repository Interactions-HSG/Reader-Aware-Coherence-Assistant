# -*- coding: utf-8 -*-
# 
from flask_cors import CORS # This is generally important for online applications where you want your APIs to be accessible by other domains.
from flask import Flask, render_template, request, jsonify, send_from_directory
import requests as rq 
from .ai_comm_utils import *

from reader_profile import fetch_abstract, fetch_profiles

from . import metrics

app = Flask(__name__)
CORS(app)

#  the is the declaration of the flask app
__all__ = ['app',
    'fetch_abstract', 
    'fetch_profiles',
    'CORS',
    'Flask', 'render_template', 'request', 'jsonify',
    'rq',
    'metrics',
    'SupportedOutputFormats','validate',
    #'score_clauses', #lesson learnt: an unuseful redundancy(see metrics) which breaks a bit the global software design
]
