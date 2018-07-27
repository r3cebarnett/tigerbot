import discord
from discord.ext import commands
import pokebase as pb

class PokemonCog:
    def __init__(self, bot):
        self.bot = bot
        self.hex_colors = {
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

        self.pretty_stat = {
            'hp': 'HP',
            'attack': 'Attack',
            'defense': 'Defense',
            'special-attack': 'Special Attack',
            'special-defense': 'Special Defense',
            'speed': 'Speed'
        }

    @commands.command(name='pp',
                    description="Link to pokemon-planet",
                    brief="Pokemon-planet",
                    pass_context=True)
    async def poke_planet(self, ctx):
        await self.bot.say("http://pokemon-planet.com/gameFullscreen.php")

    @commands.command(name="pdex",
                    description="Gives details about a specified pokemon",
                    brief="What this pokemon be",
                    pass_context=True,
                    aliases=['dex', 'pokedex', 'pokemon', 'poke'])
    async def pokedex(self, ctx, *args):
        query = ''.join(args).lower()

        try:
            poke = pb.pokemon(query)
        except ValueError as e:
            await self.bot.say(f"Sorry, {ctx.message.author.mention}, {query} was not found.")
            return

        name = poke.name.capitalize()
        spec = pb.pokemon_species(poke.id)
        color = self.hex_colors[spec.color.name]
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
            ev_text.append(f"**{self.pretty_stat[i]}**\t\t\t{evs[i]}")

        ev_text = '\n'.join(ev_text)
        embed.add_field(name="Effort Values", value=ev_text, inline=False)

        embed.add_field(name="\u200b", value="\u200b", inline=False)

        # Add stat fields
        for i in stats:
            embed.add_field(name = self.pretty_stat[i.stat.name], value=i.base_stat, inline=True)

        await self.bot.say(embed=embed)

    @commands.command(name="pnat",
                    description="Gives details about a specified pokemon",
                    brief="What this pokemon be",
                    pass_context=True,
                    aliases=["nature", "nat"])
    async def nature(self, ctx, *args):
        query = ''.join(args).lower()

        try:
            nature = pb.nature(query)
        except ValueError as e:
            await self.bot.say(f"Sorry, {ctx.message.author.mention}, {query} was not found.")
            return

        msg = f"{nature.name.capitalize()}"
        msg += f", +10% {pretty_stat[nature.increased_stat.name]}"
        msg += f", -10% {pretty_stat[nature.decreased_stat.name]}"

        await self.bot.say(msg)

def setup(bot):
    bot.add_cog(PokemonCog(bot))
