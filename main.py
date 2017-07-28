import discord
import asyncio
import configparser
import random
import time
from Imgur import Imgur
from triggered import *

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
    if message.content.startswith('!'):
        args = message.content.split(' ')

        if args[0] == '!ping':
            await client.send_message(message.channel, 'Pong!')

        elif args[0] == '!i':
            if message.channel.name == 'imgur':
                pic = imgur.get()
                await client.send_message(message.channel, pic)
            else:
                await client.send_message(message.channel, 'Use #imgur please.')

        elif args[0] == '!clear':
            valid = []
            async for check in client.logs_from(message.channel, limit=100):
                if check.author == client.user:
                    await client.delete_message(check)
                    break

        elif args[0] == '!help':
            await client.send_message(message.channel,
            """
```Current commands:\n
!ping - Test to see if the bot is working
!i - Shows a random imgur link, warning: NSFW
!clear *count - clears the last <count> messages, default: 3
!triggered - shows a random triggered image
!pick choice1 choice2 choice3 choicen - picks a random choice from the ones given```""")

        elif args[0] == '!triggered':
            with open(triggered(21), 'rb') as f:
                await client.send_file(message.channel, f)

        elif args[0] == '!pick':
            if len(args) == 1:
                await client.send_message(message.channel, "Gotta have more arguments, bud. :zzz:")
            else:
                await client.send_message(message.channel, args[random.randint(2,len(args))-1])

        elif args[0] == '!flip':
            choice = random.randint(1,2)
            if choice == 1:
                await client.send_file(message.channel, 'flip/heads.png')
            else:
                await client.send_file(message.channel, 'flip/tails.png')

try:
    client.run(token)
except ConnectionResetError as e:
    client.logout()
