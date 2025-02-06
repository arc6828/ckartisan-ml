# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from flask_cors import CORS
from ner import perform_ner_based_on_language

from routes_ner import ner_bp
from routes_nlp import nlp_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register blueprints
app.register_blueprint(ner_bp, url_prefix='/ner')
app.register_blueprint(nlp_bp, url_prefix='/nlp')

@app.route('/')
def home():
    return "Hello, Flask with Nginx!"

if __name__ == '__main__':
    app.run()