import discord
from discord.ext import commands

class HelloCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("HelloCog loaded")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

async def setup(bot):
    await bot.add_cog(HelloCog(bot))