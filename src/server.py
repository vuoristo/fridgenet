import io
from flask import Flask, Response
from flask import request
from flask import jsonify
import json
from src.tagger.photo_tagger import recognize
import time


application = Flask(__name__)

@application.route('/test', methods=['GET'])
def hello_world():
    return Response(status=200, response='Hello, world!')


@application.route('/detect', methods=['POST'])
def parse_image():
    f = request.files['file']
    filename = 'tagger/images/uploaded_file' + str(time.time()) + '.jpeg'
    f.save(filename)
    recognize(filename)
    return Response(status=200, response='Recognized')

@application.route('/inventory', methods=['POST'])
def add_to_inventory():
    # f = request.files['image']
    # f.save('tagger/uploaded_file.jpeg')
    # Mock json files containing responses from Vision API
    with open('tagger/mock_jsons/tomato.json') as json_data:
        data = json.load(json_data)
        jsonParser(data)
    with open('tagger/mock_jsons/strawberry.json') as json_data:
        data = json.load(json_data)
        jsonParser(data)
    with open('tagger/mock_jsons/cucumber.json') as json_data:
        data = json.load(json_data)
        jsonParser(data)
    return Response(status=200, response='Added')
