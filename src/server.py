import io
from flask import Flask, Response
from flask import request
from PIL import Image

app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def parse_image():
    image_data = request.data
    Image.open(io.BytesIO(image_data))
    return Response(status=200, response='tomato')
