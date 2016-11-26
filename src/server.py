import io
from flask import Flask, Response
from flask import request
from flask import jsonify
from PIL import Image

app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def parse_image():
   data = "{'stripeAmountRet': 'ripuliripuli'}"
   return jsonify(data)
