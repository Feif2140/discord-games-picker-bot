import discord
from discord.ext import commands 
import random


class other_commands(commands.Cog):
    intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
    client = commands.Bot(command_prefix = '$', intents = intents)

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online (utuber).')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} has joined a server.')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left a server')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('please review command syntax')

    @commands.command(aliases=['Ping'])
    async def ping(self, ctx):
        await ctx.send('hello!')

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question=""):
        responses = ['yes', 'no', 'perhaps', 'ask me again', 'definitely', 'never in your wildest dreams', '100%']
        if len(question)==0:
            await ctx.send(f'please ask a question')
        else: await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command()
    async def clear(self, ctx, amount=0):
        await ctx.channel.purge(limit=amount)

def setup(client):
    client.add_cog(other_commands(client))