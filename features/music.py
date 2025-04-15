import discord
from discord.ext import commands
import yt_dlp

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("MusicCog loaded")
    
    @commands.command(name='play')
    async def play(self, ctx, *, url: str):
        # Connect to vc
        vc = ctx.author.voice.channel
        if not vc:
            await ctx.send("You are not currently in a voice channel.")
            return
        await vc.connect()

        # Download audio
        ydl_ops = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'opus',
            }],
            'quiet': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_ops) as ydl:
                info = ydl.extract_info(url, download=False)
                url = info['url']
        except Exception as e:
            await ctx.send(f"Error downloading audio: {e}")
            return

        # Play audio
        try:
            vc.play(discord.FFmpegPCMAudio(url, before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'))
            await ctx.sent(f'Now playing: {info['title']}')
        except Exception as e:
            await ctx.send(f'Error playing audio: {e}')

def setup(bot):
    bot.add_cog(MusicCog(bot))