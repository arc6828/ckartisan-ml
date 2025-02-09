# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register blueprints
# from routes_ner import ner_bp
# app.register_blueprint(ner_bp, url_prefix='/ner')

from routes_nlp import nlp_bp
app.register_blueprint(nlp_bp, url_prefix='/nlp')

@app.route('/')
def home():
    return "Hello, Flask with Nginx!"

if __name__ == '__main__':
    app.run()