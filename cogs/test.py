import discord
from discord.ext import commands, tasks

class test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online (test).')

def setup(client):
    client.add_cog(test(client))
    