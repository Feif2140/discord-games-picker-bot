import discord
import json
from discord.ext import commands
import os


class gGames(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online (gGames).')

    async def addRank(self, ctx, arr, game, rank):
        await ctx.send('adding rank...')
        print('adding rank fcn')
        if (not arr.count(game)==0):
            arr = await self.delRank(ctx, arr, game)

        if (len(arr) < rank):
            arr.append(game)
            return arr
        else:
            arr.insert(rank - 1, game)
            return arr

    @commands.command()
    async def add_games(self, ctx, *, info):
        member = str(ctx.message.author)
        game = str(info.split('$')[0])
        rank = int(info.split('$')[1])

        if os.path.isfile('games2.json'):
            with open('games2.json', 'r') as f:
                data = json.load(f)
            try:
                print('running "try" block')
                pylist = data[member]['games-ranked']
                print(pylist)
                pylist = await self.addRank(ctx, pylist, game, rank)
                print(pylist)
                data[member]['games-ranked'] = pylist
                await ctx.send('done data')
            except KeyError:
                await ctx.send('running keyerror block')
                data[member] = {'games-ranked': [game]}
        else: 
            await ctx.send('no os path, running else blaock')
            data = {member: {'games-ranked': [game]}}
        with open('games2.json', 'w+') as f:
            await ctx.send('json dumping')
            json.dump(data, f, sort_keys=True, indent=4)
            await ctx.send('successful')

    async def delRank(self, ctx, arr, game):
        await ctx.send('deleting rank...')
        print('deleting rank fcn')
        if (arr.count(game) == 0):
            await ctx.send(f'{game} does not exist in your ranked games')
            return arr
        else:
            arr.remove(game)
            return arr

    @commands.command()
    async def remove_games(self, ctx, *, info):
        member = str(ctx.message.author)
        game = info

        if os.path.isfile('games2.json'):
            with open('games2.json', 'r') as f:
                data = json.load(f)
            try:
                print('running "try" block')
                pylist = data[member]['games-ranked']
                print(pylist) 
                pylist = await self.delRank(ctx, pylist, game)
                print(pylist)
                data[member]['games-ranked'] = pylist
                await ctx.send('done data')
            except KeyError:
                await ctx.send('your ranked games list is empty')
                return
        else: 
            await ctx.send('no os path, running else block')
            print('path err')
            return
        with open('games2.json', 'w+') as f:
            await ctx.send('json dumping')
            json.dump(data, f, sort_keys=True, indent=4)
            await ctx.send('successful')

    @commands.command()
    async def get_games(self, member: discord.Member):
        with open('games2.json', 'r') as f:
            data = json.load(f)
        result = data[member]['games-ranked']
        await ctx.send(' '.join(result))

    @commands.command()
    async def nuke_games(self, ctx, *, info):
        member = str(ctx.message.author)
        if (not info == "confirm"):
            await ctx.send('please type .nuke_games confirm to nuke, are you sure')
        else:
            if os.path.isfile('games2.json'):
                with open('games2.json', 'r') as f:
                    data = json.load(f)
                try:
                    print('nuking')
                    data[member]['games-ranked'] = []
                except KeyError:
                    await ctx.send('your ranked games list is empty')
                    return
            else: 
                await ctx.send('no os path, running else block')
                print('path err')
                return
            with open('games2.json', 'w+') as f:
                await ctx.send('json dumping')
                json.dump(data, f, sort_keys=True, indent=4)
                await ctx.send('successful')

    @commands.command()
    async def ordering(self, ctx, *, info):
        await ctx.send(str(info))
        await ctx.send(ctx.mentions[0].id)

    

def setup(client):
    client.add_cog(gGames(client))
