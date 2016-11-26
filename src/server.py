import io
import os
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
    filename = 'src/tagger/uploaded_images/uploaded_file' + str(time.time()) + '.jpeg'
    f.save(filename)
    ret = recognize(filename)
    if ret is not None:
        return Response(status=200, response=ret)
    else:
        return Response(status=204, response='Not recognized')

@application.route('/inventory', methods=['GET'])
def get_inventory():
    with open('src/tagger/inventory.txt', 'r') as f:
        inventory = f.read()
        items = [item.strip() for item in inventory.split("\n") if item]
        return Response(status=200, response=json.dumps(items), content_type='application/javascript')

@application.route('/inventory', methods=['DELETE'])
def del_inventory():
    with open('src/tagger/inventory.txt', 'w') as f:
        inventory = f.read()
        items = [item.strip() for item in inventory.split("\n") if item]
        label = request.json.get('label', None)
        if label is not None:
            if label in items:
                items.remove(items.index(label))

        for item in items:
            f.write(item + os.linesep)
        return Response(status=200)
