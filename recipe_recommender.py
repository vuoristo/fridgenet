import requests
import json

X_MASHAPE_KEY = ""
API_KEY = ""

def get_recipes_for_items(list_of_items):
  headers={
    "X-Mashape-Key": X_MASHAPE_KEY,
    "Accept": "application/json"
  }
  payload = {'q':','.join(list_of_items), 'key': API_KEY}
  r = requests.get("https://community-food2fork.p.mashape.com/search", params=payload, headers=headers)

  r_dict = json.loads(r.text)
  if 'recipes' in r_dict:
    rids = [rec['recipe_id'] for rec in r_dict['recipes']]
  else:
    return None

  return rids

def get_recipe(rid):
  headers={
    "X-Mashape-Key": X_MASHAPE_KEY,
    "Accept": "application/json"
  }
  payload = {'rId':rid, 'key': API_KEY}
  r = requests.get("https://community-food2fork.p.mashape.com/get", params=payload, headers=headers)
  r_dict = json.loads(r.text)

  return r_dict

rids = get_recipes_for_items(['mozzarella'])

import pprint as pp
for rid in rids:
  rec = get_recipe(rid)
  pp.pprint(rec)
