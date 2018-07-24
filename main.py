import random
import asyncio
import configparser
import pokebase as pb
import discord

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
            await client.say(f"Congratulations, {context.message.author.mention}!\n{HS.get_image()}")
            HS.get_rand()
            await client.say(HS.guess_print())
        else:
            await client.say(f"Incorrect guess: {guess}, {context.message.author.mention}")
    else:
        await client.say(f"Sorry, {context.message.author.mention}, there isn't a current card out. Try !card or !c to guess a new card!")

@client.command(name='8ball',
                description="Magic 8 ball",
                brief="Magic 8 ball",
                aliases=['8','8b'],
                pass_context=True)
async def eight_ball(context):
    answers = ["As I see it, yes",
                "Ask again later",
                "Better not tell you now",
                "Cannot predict now",
                "Concentrate and ask again",
                "Don’t count on it",
                "It is certain",
                "It is decidedly so",
                "Most likely",
                "My reply is no",
                "My sources say no",
                "Outlook good",
                "Outlook not so good",
                "Reply hazy try again",
                "Signs point to yes",
                "Very doubtful",
                "Without a doubt",
                "Yes",
                "Yes, definitely",
                "You may rely on it"]

    await client.say(f"{random.choice(answers)}, {context.message.author.mention}")

@client.command(name='pp',
                description="Link to pokemon-planet",
                brief="Pokemon-planet",
                pass_context=True)
async def poke_planet(context):
    await client.say("http://pokemon-planet.com/gameFullscreen.php")

@client.command(name="dex",
                description="Gives details about a specified pokemon",
                brief="What this pokemon be",
                pass_context=True)
async def pokedex(context, *args):
    hex_colors = {
        "black": 0x000000,
        "blue": 0x0000ff,
        "brown": 0xa52a2a,
        "gray": 0xbebebe,
        "green": 0x00ff00,
        "pink": 0xff69b4,
        "purple": 0x9b30ff,
        "red": 0xff0000,
        "white": 0xffffff,
        "yellow": 0xffff00
    }

    pretty_stat = {
        'hp': 'HP',
        'attack': 'Attack',
        'defense': 'Defense',
        'special-attack': 'Special Attack',
        'special-defense': 'Special Defense',
        'speed': 'Speed'
    }

    query = ''.join(args).lower()

    try:
        poke = pb.pokemon(query)
    except ValueError as e:
        await client.say(f"Sorry, {context.message.author.mention}, {query} was not found.")
        return

    name = poke.name.capitalize()
    spec = pb.pokemon_species(poke.id)
    color = hex_colors[spec.color.name]
    stats = poke.stats
    ico_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png"
    stats.reverse()

    #Find flavor text
    big_flav = spec.flavor_text_entries
    flav = "No suitable flavor text found."

    for i in big_flav:
        if i.language.name == "en":
            flav = i.flavor_text
            break

    embed = discord.Embed(colour=discord.Colour(color), description=flav)

    embed.set_thumbnail(url=poke.sprites.front_default)
    embed.set_author(name=f"{poke.name.capitalize()}, Pokémon #{poke.id}", url="https://pokeapi.co", icon_url=ico_url)
    embed.set_footer(text="All information is sourced from https://pokeapi.co/", icon_url=ico_url)

    #Add type
    types = []

    for i in poke.types:
        types.append(f"**{i.type.name.capitalize()}**")

    type_text = '/'.join(types)
    embed.add_field(name="Type", value=type_text, inline=False)

    embed.add_field(name="\u200b", value="\u200b", inline=False)

    #Add effort values
    evs = {}
    for i in stats:
        if i.effort > 0:
            evs[i.stat.name] = i.effort

    ev_text = []

    for i in list(evs.keys()):
        ev_text.append(f"**{pretty_stat[i]}**\t\t\t{evs[i]}")

    ev_text = '\n'.join(ev_text)
    embed.add_field(name="Effort Values", value=ev_text, inline=False)

    embed.add_field(name="\u200b", value="\u200b", inline=False)

    # Add stat fields
    for i in stats:
        embed.add_field(name = pretty_stat[i.stat.name], value=i.base_stat, inline=True)

    await client.say(embed=embed)

try:
    client.run(TOKEN)
except ConnectionResetError as e:
    client.logout()
