import discord
from discord.ext import commands
import ollama

class AskCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("AskCog loaded")
        self.model = "llama3.2"  # Default model name

    async def load_model(self, ctx):
        try:
            ollama.show(self.model)
        except ollama.ResponseError:
            await ctx.send(f"⏳ Downloading `{self.model}`... (This may take a while)")
            ollama.pull(self.model)
            await ctx.send("✅ Model ready!")

    @commands.command(name='ask')
    async def ask(self, ctx, *, question: str):
        await self.load_model(ctx)
        """Ask a question to the Ollama model."""
        try:
            response = ollama.generate(
                model=self.model,
                prompt=question,
            )
            await ctx.send(response['response'])
        except Exception as e:
            await ctx.send(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(AskCog(bot))