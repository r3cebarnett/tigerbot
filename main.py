import discord
import asyncio
import configparser
from Imgur import Imgur

config = configparser.ConfigParser()
config.read('config.cfg')
username = config.get('bot','username')
userid = config.get('bot','userid')
token = config.get('bot','token')

client = discord.Client()

imgur = Imgur()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))

    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
    elif message.content.startswith('!i'):
        pic = imgur.get()
        await client.send_message(message.channel, pic)

client.run(token)
