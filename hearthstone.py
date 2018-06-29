import requests
import json
import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

response = requests.get("https://omgvamp-hearthstone-v1.p.mashape.com/cards",
  headers={
    "X-Mashape-Key": config.get('hearthstone', 'api')
  }
)

data = json.loads(response.text) # Note that this is a dict now
print(data.keys()) # gives all the categories
