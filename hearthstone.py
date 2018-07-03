import requests
import json
import configparser
import random

class Hearthstone:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.cfg')
        self.card = None
        self.still_looking = False

        self.response = requests.get("https://omgvamp-hearthstone-v1.p.mashape.com/cards?collectible=1",
          headers={
            "X-Mashape-Key": config.get('hearthstone', 'api')
          }
        )

        self.data = json.loads(self.response.text)
        self.keys = list(self.data.keys())

        for i in range(len(self.keys)):
            if len(self.data[self.keys[i]]) == 0 or self.keys[i] == 'Hero Skins':
                self.data.pop(self.keys[i], None)

        self.keys = list(self.data.keys())

    def guess_print(self):
        str = ""
        str += "This card is a {} {} that is {}.\n".format(self.card['cardSet'],
                                                            self.card['type'],
                                                            self.card['rarity'])

        if self.card['type'] is not 'Spell':
            str += "It is a {} mana {}/{}.\n".format(self.card['cost'],
                                                    self.card['health'],
                                                    self.card['attack'])
        else:
            str += "It costs {} mana.\n".format(self.card['cost'])

        str += "\"{}\"\n".format(self.card['flavor'])
        if 'race' in list(self.card.keys()):
            str += "Tribe: {}\n".format(self.card['race'])

        return str

    def get_image(self):
        return self.card['img']

    def get_rand(self):
        cardClass = random.choice(self.keys)
        cards = self.data[cardClass]
        self.card = random.choice(cards)
        self.still_looking = True