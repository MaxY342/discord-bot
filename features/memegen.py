import discord
from discord.ext import commands
import praw

class MemeGen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(
            client_id='YOUR_CLIENT_ID',
            client_secret = 'YOUR_CLIENT_SECRET',
            
        )