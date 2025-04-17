import discord
from discord.ext import commands
import yt_dlp
from collections import deque

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}
        print("MusicCog loaded")

    def get_queue(self, ctx):
        if not ctx.guild.id in self.queues:
            self.queues[ctx.guild.id] = deque()
        return self.queues[ctx.guild.id]

    async def play_next(self, ctx):
        queue = self.get_queue(ctx)
        if not queue:
            await ctx.send("The queue is empty.")
            return
        
        url, title = queue.popleft()
        vc = ctx.voice_client

        try:
            vc.play(
                discord.FFmpegPCMAudio(
                    url,
                    before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
                    ),
                    after=lambda e: self.bot.loop.create_task(self.play_next(ctx))
                )
            await ctx.send(f'Now playing: {title}')
        except Exception as e:
            await ctx.send(f'Error playing audio: {e}')
            await self.play_next(ctx)

    @commands.command(name='play')
    async def play(self, ctx, *, url: str):
        # Connect to vc
        if not ctx.author.voice:
            await ctx.send("You are not in a voice channel!")
            return
        vc = await ctx.author.voice.channel.connect()
        if ctx.voice_client:
            await ctx.send("moved to {vc.channel.name}")
        
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
                audio_url = info['url']
        except Exception as e:
            await ctx.send(f"Error downloading audio: {e}")
            return

        # Add song to queue
        queue = self.get_queue(ctx)
        queue.append((audio_url, info['title']))
        if ctx.voice_client.is_playing():
            await ctx.send(f'Added to queue: {info["title"]}')
        else:
            await self.play_next(ctx)

    @commands.command(name='search')
    async def search(self, ctx, *, query: str):
        ydl_ops = {
            'format': 'bestaudio/best',
            'quiet': True,
            'extract_flat': True,
            'default_search': 'ytsearch5',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_ops) as ydl:
                info = ydl.extract_info(f'ytsearch5:{query}', download=False)
                if len(info['entries']) == 0:
                    await ctx.send("No results found.")
                    return
                for entry in info['entries']:
                    await ctx.send(f"Title: {entry['title']} Channel: {entry['channel']} Url: {entry['url']}", suppress_embeds=True)
        except Exception as e:
            await ctx.send(f"Error searching: {e}")

    @commands.command(name="queue")
    async def queue(self, ctx):
        queue = self.queues.get(ctx.guild.id)
        if not queue:
            await ctx.send("The queue is empty.")
            return
        queue_list = [title for _, title in queue]
        await ctx.send(f"Queue: {queue_list}")

    @commands.command(name='skip')
    async def skip(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            await ctx.send("No audio is currently playing.")
            return
        vc.stop()
        await ctx.send("Skipped.")
    
    @commands.command(name='clear')
    async def clear(self, ctx):
        ctx.voice_client.stop()
        queue = self.get_queue(ctx)
        queue.clear()
        await ctx.send("Cleared the queue.")

async def setup(bot):
    await bot.add_cog(MusicCog(bot))