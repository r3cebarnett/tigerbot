import random
import asyncio
import configparser

from Imgur import Imgur
from hearthstone import Hearthstone
from discord.ext.commands import Bot
from os import listdir
from os.path import isfile, join

config = configparser.ConfigParser()
config.read('config.cfg')

BOT_PREFIX = "!"
TOKEN = config.get('bot', 'token')
TRIG_PATH = config.get('pictures', 'triggered')
FLIP_PATH = config.get('pictures', 'flip')

client = Bot(command_prefix=BOT_PREFIX, pm_help=True)

IMGUR = Imgur()
HS = Hearthstone()
random.seed()

trig_files = [f for f in listdir(TRIG_PATH) if isfile(join(TRIG_PATH, f))]

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
    if context.message.server is None or context.message.channel.name == 'imgur':
        pic = await IMGUR.get()
        await client.send_message(context.message.channel, pic)
    else:
        await client.say('Use #imgur please.')

@client.command(name='triggered',
                description="Posts a random triggered picture",
                brief="Triggered?",
                aliases=['t', 'trig'],
                pass_context=True)
async def triggered(context):
    selection = random.choice(trig_files)
    with open(TRIG_PATH + selection, 'rb') as f:
        await client.send_file(context.message.channel, f)

@client.command(name='pick',
                description="Pick between n many arguments separated by spaces",
                brief="Difficulty making a choice?",
                aliases=['p'],
                pass_context=True)
async def pick(context, args):
    if len(args) == 0:
        await client.say("Gotta have more arguments, " + context.message.author)
    else:
        await client.say(random.choice(args))

@client.command(name='flip',
                description="Heads or tails?",
                brief="Heads or tails?",
                aliases=['f'],
                pass_context=True)
async def flip(context):
    choice = random.choice(['heads.png', 'tails.png'])
    await client.send_file(context.message.channel, FLIP_PATH + choice)

@client.command(name='card',
                description="Get a hearthstone card to guess",
                brief="Guess the card!",
                aliases=['c'],
                pass_context=True)
async def hs_get(context):
    if context.message.channel.name != 'hs-game':
        return
    if HS.still_looking:
        await client.say(HS.guess_print())
    else:
        HS.get_rand()
        await client.say(HS.guess_print())

@client.command(name='guess',
                description="Guess the current HS trivia card",
                brief="Make a guess!",
                aliases=['g'],
                pass_context=True)
async def hs_guess(context, *args):
    if context.message.channel.name != 'hs-game':
        return
    if HS.still_looking:
        guess = ' '.join(args)
        if HS.check_guess(guess):
            await client.say(f"Congratulations, {context.message.author.mention}!")
            await client.say(HS.get_image())
        else:
            await client.say(f"Incorrect guess: {guess}, {context.message.author.mention}")
    else:
        await client.say(f"Sorry, {context.message.author.mention}, there isn't a current card out. Try !card or !c to guess a new card!")

try:
    client.run(TOKEN)
except ConnectionResetError as e:
    client.logout()
