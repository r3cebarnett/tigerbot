import requests
import json
import configparser
import random

"""
{
'name': 'Booty Bay Bodyguard',
'cardSet': 'Basic',
'type': 'Minion',
'rarity': 'Free',
'cost': 5,
'attack': 5,
'health': 4,
'text': '<b>Taunt</b>',
'flavor': 'You can hire him... until someone offers him enough gold to turn on you.',
'playerClass': 'Neutral',
only at end 'img': 'http://media.services.zam.com/v1/media/byName/hs/cards/enus/CS2_187.png',
'mechanics': [{'name': 'Taunt'}]}
CONDITIONAL RACE for TRIBE
"""

config = configparser.ConfigParser()
config.read('config.cfg')

response = requests.get("https://omgvamp-hearthstone-v1.p.mashape.com/cards?collectible=1",
  headers={
    "X-Mashape-Key": config.get('hearthstone', 'api')
  }
)

data = json.loads(response.text) # Note that this is a dict now
keys = list(data.keys())

for i in range(len(keys)):
    if len(data[keys[i]]) == 0 or keys[i] == 'Hero Skins':
        data.pop(keys[i], None)

keys = list(data.keys())

""" At this point we have all cards that can be called now """

cardClass = random.choice(keys)
cards = data[cardClass]
card = random.choice(cards)

print(card)

""" Now we have a specified card """
