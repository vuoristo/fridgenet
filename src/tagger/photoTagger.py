import json
import os


#Checks if the labels in the response match any of the accepted
def jsonParser(data):
    with open('tagger/foods.txt') as f:
        food_list = f.read().splitlines()
    label_annotations = data["labelAnnotations"]
    for annotation in label_annotations:
        label = annotation["description"]
        if(label in food_list):
            with open('tagger/inventory.txt', 'a') as f1:
                f1.write(label + os.linesep)
