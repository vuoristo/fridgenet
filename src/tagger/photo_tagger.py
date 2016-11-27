import json
import os
import argparse
import base64

from googleapiclient import discovery

#Checks if the labels in the response match any of the accepted
def jsonParser(label_dict):
    with open('src/tagger/foods.txt') as f:
        food_list = f.read().splitlines()
    for annotation in label_dict:
        label = annotation["description"].lower()
        if label in food_list:
            return label
    return None

def recognize(filename):
    service = discovery.build('vision', 'v1', developerKey=os.environ.get("GOOGLE_API_KEY"))
    with open(filename, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 5
                }]
            }]
        })
        response = service_request.execute()
        ret = jsonParser(response['responses'][0]['labelAnnotations'])
        return ret

