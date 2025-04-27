import discord
from discord.ext import commands
import pokebase as pb
import random

class PokemonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='pokemon_info')
    async def get_pokemon(self, ctx, *, name:str):
        pokemon = pb.pokemon(name.lower())
        if not pokemon:
            await ctx.send(f"No pokemon found for {name}.")
            return

        embed = discord.Embed(title=pokemon.name.capitalize(), color=0x00ff00)
        embed.set_thumbnail(url=pokemon.sprites.front_default)
        embed.add_field(name="Height", value=pokemon.height, inline=True)
        embed.add_field(name="Weight", value=pokemon.weight, inline=True)
        embed.add_field(name="Base Experience", value=pokemon.base_experience, inline=True)
        embed.add_field(name="Types", value=", ".join([t.type.name for t in pokemon.types]), inline=True)
        embed.add_field(name="Abilities", value=", ".join([a.ability.name for a in pokemon.abilities]), inline=True)
        embed.add_field(name="Stats", value="\n".join([f"{s.stat.name}: {s.base_stat}" for s in pokemon.stats]), inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name='random_pokemon')
    async def random_pokemon(self, ctx):
        """Get a random Pokémon."""
        try:
            pokemon = pb.pokemon(random.randint(1, len(pb.APIResourceList('pokemon'))))
            possible_moves = [m.move.name for m in pokemon.moves]
            move1 = possible_moves.pop(random.randint(0, len(possible_moves) - 1))
            move2 = possible_moves.pop(random.randint(0, len(possible_moves) - 1))
            move3 = possible_moves.pop(random.randint(0, len(possible_moves) - 1))
            move4 = possible_moves.pop(random.randint(0, len(possible_moves) - 1))
            moves = [move1, move2, move3, move4]

            embed = discord.Embed(title=pokemon.name.capitalize(), color=0x00ff00)
            embed.set_thumbnail(url=pokemon.sprites.front_default)
            embed.add_field(name="Height", value=pokemon.height, inline=True)
            embed.add_field(name="Weight", value=pokemon.weight, inline=True)
            embed.add_field(name="Base Experience", value=pokemon.base_experience, inline=True)
            embed.add_field(name="Types", value=", ".join([t.type.name for t in pokemon.types]), inline=True)
            embed.add_field(name="Abilities", value=", ".join([a.ability.name for a in pokemon.abilities]), inline=True)
            embed.add_field(name="Moves", value=", ".join(moves[:4]), inline=True)
            embed.add_field(name="Stats", value="\n".join([f"{s.stat.name}: {s.base_stat}" for s in pokemon.stats]), inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(PokemonCog(bot))

