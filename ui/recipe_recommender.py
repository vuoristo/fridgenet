import requests
import json
import os

X_MASHAPE_KEY = "KqHWb2rYKImshtwo9BeupImaWkwfp1BQTq7jsnAU2R80mVzO6N"
API_KEY = 'c1827c33a6a2a89006d3a4a84d30ea98'

def get_recipes_for_items(list_of_items):
  headers={
    "X-Mashape-Key": os.environ.get('MASHAPE_KEY'),
    "Accept": "application/json"
  }
  payload = {'q':','.join(list_of_items), 'key': os.environ.get('API_KEY')}
  r = requests.get("https://community-food2fork.p.mashape.com/search", params=payload, headers=headers)

  r_dict = json.loads(r.text)
  if 'recipes' in r_dict:
    rids = [rec['recipe_id'] for rec in r_dict['recipes']]
  else:
    return None

  return rids

def get_recipe(rid):
  headers={
    "X-Mashape-Key": os.environ.get('MASHAPE_KEY'),
    "Accept": "application/json"
  }
  payload = {'rId':rid, 'key': os.environ.get('API_KEY')}
  r = requests.get("https://community-food2fork.p.mashape.com/get", params=payload, headers=headers)
  r_dict = json.loads(r.text)

  return r_dict

