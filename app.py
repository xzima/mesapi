#!/usr/bin/env python3

import os
from conf.config import DEF_TEXT
from function.sendmes import sendmes_telegram
from function.senddoc import senddoc_telegram
from flask import Flask, request, Response, render_template
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
# app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/api/mes', methods=['GET'])
def message():
    query_parameters = request.args
    text = query_parameters.get('text', default=DEF_TEXT)
    chat_id = query_parameters.get('chat_id', default=os.getenv('DEF_CHAT_ID'))
    sendmes_telegram(text, chat_id)
    return Response(status=200)

@app.route('/api/doc', methods=['GET', 'POST'])
def document():
    document = request.files['document']
    query_parameters = request.args
    chat_id = query_parameters.get('chat_id', default=os.getenv('DEF_CHAT_ID'))
    caption = query_parameters.get('caption')
    senddoc_telegram(document, chat_id, caption)
    return Response(status=200)

@app.route('/swagger.yaml')
def send_static():
    return render_template('swagger.yaml')

SWAGGER_URL = '/api'
API_URL = '/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "MesAPI",
        'layout': "BaseLayout"
    },
)

app.register_blueprint(swaggerui_blueprint)

app.run(host='0.0.0.0', port='8080')