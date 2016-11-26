import io
from flask import Flask, Response
from flask import request
from flask import jsonify
import json
from tagger.photoTagger import jsonParser

application = Flask(__name__)

@application.route('/test', methods=['GET'])
def hello_world():
    return Response(status=200, response='Hello, world!')


@application.route('/detect', methods=['POST'])
def parse_image():
    f = request.files['image']
    f.save('tagger/uploaded_file.jpeg')
    return Response(status=200, response='Detected')

@application.route('/inventory', methods=['GET'])
def get_inventory():
    with open('src/tagger/inventory.txt', 'r') as f:
        inventory = f.read()
        items = [item.strip() for item in inventory.split("\n") if item]
        return Response(status=200, response=json.dumps(items), content_type='application/javascript')

@application.route('/inventory', methods=['POST'])
def add_to_inventory():
    # f = request.files['image']
    # f.save('tagger/uploaded_file.jpeg')
    # Mock json files containing responses from Vision API
    with open('src/tagger/mock_jsons/tomato.json') as json_data:
        data = json.load(json_data)
        jsonParser(data)
    with open('src/tagger/mock_jsons/strawberry.json') as json_data:
        data = json.load(json_data)
        jsonParser(data)
    with open('src/tagger/mock_jsons/cucumber.json') as json_data:
        data = json.load(json_data)
        jsonParser(data)
    return Response(status=200, response='Added')
