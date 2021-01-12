import discord
from discord.ext import commands, tasks
from itertools import cycle

class status(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is oline (status).')

def setup(client):
    client.add_cog(status(client))