import discord
import os
from discord.ext import commands
    

client = commands.Bot(command_prefix = '$')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    print(os.listdir)
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run ('NzkyMTIyMjI5NTcxNTg0MDQy.X-ZHUA.fNphVKY5EhyIRI6MhGRLCTu0IZE')

