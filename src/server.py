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

@application.route('/inventory', methods=['GET'])
def get_inventory():
    with open('src/tagger/inventory.txt', 'r') as f:
        inventory = f.read()
        items = [item.strip() for item in inventory.split("\n") if item]
        return Response(status=200, response=json.dumps(items), content_type='application/javascript')

