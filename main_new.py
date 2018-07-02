import random
import asyncio
import configparser
from discord.ext.commands import Bot

config = configparser.ConfigParser()
config.read('config.cfg')

BOT_PREFIX = "!"
TOKEN = config.get('bot', 'token')

client = Bot(command_prefix=BOT_PREFIX, pm_help=True)

imgur = Imgur()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')

@client.command(name='ping',
                description="Tests reactivity",
                brief="Am I working?")
async def ping():
    await client.say('Pong!')

@client.command(name='imgur',
                description="Posts a random picture from Imgur, warning NSFW",
                brief="NSFW Warning - Random Pictures",
                aliases=['i'],
                pass_context=True)
async def imgur(context):
    if context.message.channel.name == 'imgur':
        pic = imgur.get()
        await client.send_message(message.channel, pic)
    else:
        await client.say('Use #imgur please.')

@client.command()
async def
