import discord
from discord.ext import commands

class example(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online (example).')

    @commands.command()
    async def woaw(self, ctx):
        await ctx.send('Pong!')

def setup(client):
    client.add_cog(example(client))
    