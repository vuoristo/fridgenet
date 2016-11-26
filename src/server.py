import io
from flask import Flask, Response
from flask import request
from flask import jsonify

application = Flask(__name__)

@application.route('/test', methods=['GET'])
def hello_world():
    return Response(status=200, response='Hello, world!')


@application.route('/detect', methods=['POST'])
def parse_image():
    list = [
        {'param': 'foo', 'val': 2},
        {'param': 'bar', 'val': 10}
    ]
    return jsonify(results=list)
