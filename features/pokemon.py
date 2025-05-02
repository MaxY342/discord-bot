import discord
from discord.ext import commands
import pokebase as pb
import random
import sqlite3

class PokemonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.con = sqlite3.connect('pokemon.db')
        self.cur = self.con.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS user_pokemon (id INTEGER, pokemon TEXT)')
        self.cur.execute('CREATE TABLE IF NOT EXISTS pokemon_moves (id INTEGER, pokemon TEXT, move TEXT)')
        self.load_pokemon_rarity_groups()
    
    def load_pokemon_rarity_groups(self):
        species_list = pb.APIResourceList('pokemon-species')
        self.rarity_groups = {
            'common': [],
            'uncommon': [],
            'rare': [],
            'legendary': []
        }
        for species in species_list:
            if species.capture_rate >= 181:
                self.rarity_groups['common'].append(species.name)
            elif species.capture_rate >= 91:
                self.rarity_groups['uncommon'].append(species.name)
            elif species.capture_rate >= 31:
                self.rarity_groups['rare'].append(species.name)
            else:
                self.rarity_groups['legendary'].append(species.name)

    def pokemon_gacha(self, common_prob, uncommon_prob, rare_prob):
        random = random.randint(1, 100)
        if random <= common_prob:
            rarity = 'common'
            pokemon = random.choice(self.rarity_groups['common'])
        elif random <= (common_prob + uncommon_prob):
            rarity = 'uncommon'
            pokemon = random.choice(self.rarity_groups['uncommon'])
        elif random <= (common_prob + uncommon_prob + rare_prob):
            rarity = 'rare'
            pokemon = random.choice(self.rarity_groups['rare'])
        else:
            rarity = 'legendary'
            pokemon = random.choice(self.rarity_groups['legendary'])
        return (pokemon, rarity)
    
    async def pokemon_caught_embed(self, pokemon, rarity, moves, ctx):
        rarity_color = self.get_rarity_color(rarity)
        embed = discord.Embed(title=f"You caught a {rarity} Pokémon!", color=rarity_color)
        embed.add_field(name="Pokémon", value=pokemon.name.capitalize(), inline=True)
        embed.add_field(name="Moves", value=", ".join(moves), inline=True)
        embed.set_thumbnail(url="pokemon.sprites.front_default")
        embed.set_footer(text=f"Use !pokemon_info <{pokemon.name}> to see more details.")
        await ctx.send(embed=embed)

    
    def moves_gacha(self, pokemon_name):
        pokemon = pb.pokemon(pokemon_name.lower())
        possible_moves = [m.move.name for m in pokemon.moves]
        move1 = possible_moves.pop(random.randint(0, len(possible_moves) - 1))
        move2 = possible_moves.pop(random.randint(0, len(possible_moves) - 1))
        move3 = possible_moves.pop(random.randint(0, len(possible_moves) - 1))
        move4 = possible_moves.pop(random.randint(0, len(possible_moves) - 1))
        return [move1, move2, move3, move4]
    
    def add_pokemon_to_db(self, user_id, pokemon_name, moves):
        self.cur.execute('INSERT INTO user_pokemon (id, pokemon) VALUES (?, ?)', (user_id, pokemon_name))
        for move in moves:
            self.cur.execute('INSERT INTO pokemon_moves (id, pokemon, move) VALUES (?, ?, ?)', (user_id, pokemon_name, move))')
        self.con.commit()

    def get_rarity_color(self, rarity):
        if rarity == 'common':
            return 0x808080
        elif rarity == 'uncommon':
            return 0x00ff00
        elif rarity == 'rare':
            return 0xa020f0
        else:
            return 0xffd700
        
    @commands.command(name='pokemon_info')
    async def pokemon_info(self, ctx, *, name:str):
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
    
    @commands.command(name='pokeball_catch')
    async def pokeball_catch(self, ctx):
        try:
            pokemon, rarity = self.pokemon_gacha(70, 20, 7)
            moves = self.moves_gacha(pokemon)
            pokemon = pb.pokemon(pokemon.lower())
            self.pokemon_caught_embed(pokemon, rarity, moves, ctx)
            self.add_pokemon_to_db(ctx.author.id, pokemon.name, moves)
        except Exception as e:
            await ctx.send(f"Error: {e}")
    
    @commands.command(name='greatball_catch')
    async def greatball_catch(self, ctx):
        try:
            pokemon, rarity = self.pokemon_gacha(50, 30, 15)
            moves = self.moves_gacha(pokemon)
            pokemon = pb.pokemon(pokemon.lower())
            self.pokemon_caught_embed(pokemon, rarity, moves, ctx)
            self.add_pokemon_to_db(ctx.author.id, pokemon.name, moves)
        except Exception as e:
            await ctx.send(f"Error: {e}")
    
    @commands.command(name='ultraball_catch')
    async def ultraball_catch(self, ctx):
        try:
            pokemon, rarity = self.pokemon_gacha(30, 40, 20)
            moves = self.moves_gacha(pokemon)
            pokemon = pb.pokemon(pokemon.lower())
            self.pokemon_caught_embed(pokemon, rarity, moves, ctx)
            self.add_pokemon_to_db(ctx.author.id, pokemon.name, moves)
        except Exception as e:
            await ctx.send(f"Error: {e}")
    
    @commands.command(name='masterball_catch')
    async def masterball_catch(self, ctx):
        try:
            pokemon, rarity = self.pokemon_gacha(10, 40, 25)
            moves = self.moves_gacha(pokemon)
            pokemon = pb.pokemon(pokemon.lower())
            self.pokemon_caught_embed(pokemon, rarity, moves, ctx)
            self.add_pokemon_to_db(ctx.author.id, pokemon.name, moves)
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.command(name='view_pokemon')
    async def view_pokemon(self, ctx):
        pokemon = self.cur.execute('SELECT pokemon FROM user_pokemon WHERE id = ?', (ctx.author.id,)).fetchall()
        if not pokemon:
            await ctx.send("You have no Pokémon.")
            return
        embed = discord.Embed(title=f"{ctx.author.name}'s Pokémon", color=0x00ff00)
        for p in pokemon:
            moves = self.cur.execute('SELECT move FROM pokemon_moves WHERE id = ? AND pokemon = ?', (ctx.author.id, p[0])).fetchall()
            moves = [m[0] for m in moves]
            embed.add_field(name=p[0], value=", ".join(moves), inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PokemonCog(bot))

