# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from ner import perform_ner_based_on_language

from routes_ner import ner_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(ner_bp, url_prefix='/ner')

@app.route('/')
def home():
    return "Hello, Flask with Nginx!"

if __name__ == '__main__':
    app.run()