import string
import random
import requests
import asyncio

class Imgur:
    def __init__(self, id_length=5):
        self.id_length = id_length
        self._valid_characters = string.ascii_letters + string.digits
        self._base_url = 'https://i.imgur.com/{}.png'
        self._removed_url = 'https://i.imgur.com/removed.png'

    async def get(self):
        while True:
            image_id = ''.join(random.choice(self._valid_characters) for _ in range(self.id_length))
            image_url = self._base_url.format(image_id)

            r = requests.get(image_url)

            if r is not None:
                r.close()

            if r.url != self._removed_url:
                return image_url
