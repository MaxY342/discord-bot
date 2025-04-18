import discord
from discord.ext import commands

class HelloCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("HelloCog loaded")
    
    @commands.command(name='hello')
    async def hello(self, ctx):
        await ctx.send('Hello!')

async def setup(bot):
    await bot.add_cog(HelloCog(bot))