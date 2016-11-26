import io
from flask import Flask, Response
from flask import request
from flask import jsonify
from PIL import Image

app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def parse_image():
    list = [
        {'param': 'foo', 'val': 2},
        {'param': 'bar', 'val': 10}
    ]
    return jsonify(results=list)
