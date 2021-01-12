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
        if (not arr.count(game)==0):
            arr = await self.delRank(ctx, arr, game)
        if (len(arr) < rank):
            arr.append(game)
            return arr
        else:
            arr.insert(rank - 1, game)
            return arr

    @commands.command(aliases=['addG', 'addGames'])
    async def add_games(self, ctx, *, info = ''):
        if (info== ''):
            await ctx.send('please format your command like this : $addGame <game>$<rank>')
        member = str(ctx.message.author)
        game = str(info.split('$')[0])
        rank = int(info.split('$')[1])

        if os.path.isfile('games2.json'):
            with open('games2.json', 'r') as f:
                data = json.load(f)
            try:
                pylist = data[member]['games-ranked']
                pylist = await self.addRank(ctx, pylist, game, rank)
                data[member]['games-ranked'] = pylist
            except KeyError:
                data[member] = {'games-ranked': [game]}
        else: 
            data = {member: {'games-ranked': [game]}}
        with open('games2.json', 'w+') as f:
            json.dump(data, f, sort_keys=True, indent=4)
        await ctx.send('game added')

    async def delRank(self, ctx, arr, game):
        await ctx.send('deleting rank...')
        if (arr.count(game) == 0):
            await ctx.send(f'{game} does not exist in your ranked games')
            return arr
        else:
            arr.remove(game)
            return arr

    @commands.command(aliases=['delGame', 'delgames', 'deletegame', 'deletegames'])
    async def remove_games(self, ctx, *, info=''):
        member = str(ctx.message.author)
        game = info
        if (game==''):
            await ctx.send('no game selected')
        if os.path.isfile('games2.json'):
            with open('games2.json', 'r') as f:
                data = json.load(f)
            try:
                pylist = data[member]['games-ranked']
                pylist = await self.delRank(ctx, pylist, game)
                data[member]['games-ranked'] = pylist
                await ctx.send('done data')
            except KeyError:
                await ctx.send('your ranked games list is empty')
                return
        else: 
            await ctx.send('no os path, running else block')
            return
        with open('games2.json', 'w+') as f:
            await ctx.send('json dumping')
            json.dump(data, f, sort_keys=True, indent=4)
        await ctx.send('game added succesfully')

    @commands.command(aliases=['eraseGames'])
    async def erase_games(self, ctx, *, info = ""):
        member = str(ctx.message.author)
        if (not info == "confirm"):
            await ctx.send('please type .eraseGames <confirm> , are you sure')
        else:
            if os.path.isfile('games2.json'):
                with open('games2.json', 'r') as f:
                    data = json.load(f)
                try:
                    data[member]['games-ranked'] = []
                except KeyError:
                    await ctx.send('your ranked games list is empty')
                    return
            else: 
                return
            with open('games2.json', 'w+') as f:
                json.dump(data, f, sort_keys=True, indent=4)
        await ctx.send('you have succesfully deleted all your ranked games')


    @commands.command()
    async def ordering(self, ctx, *, info):
        await ctx.send(str(info))
        await ctx.send(ctx.mentions[0].id)

    @commands.command(aliases=['getGames'])
    async def get_games(self, ctx, *, mssge = ""):
        if (not len(mssge)==0):
            i = 0
            while ctx.message.mentions[i] is not None:
                member = str(ctx.message.mentions[i])
                await ctx.send('member : ' + member)
                with open('games2.json', 'r') as f:
                    data = json.load(f)
                result = data[member]['games-ranked']
                await ctx.send(', '.join(result))
                i = i+1
        else:
            member = str(ctx.message.author)
            await ctx.send('member = ' + member)
            with open('games2.json', 'r') as f:
                data = json.load(f)
            result = data[member]['games-ranked']
            await ctx.send(', '.join(result))       


    @commands.command()
    async def listofGames(self, ctx, *, pings):
        max = await self.max_games(ctx, pings)
        result = await self.compute_list(ctx, pings, max)
        result = [x[1] for x in reversed(result)]
        await ctx.send(', '.join(result))

    
    async def mastergames_list(self, ctx, pings):
        i = 0
        master = []
        while i<len(ctx.message.mentions):
            member = str(ctx.message.mentions[i])
            with open('games2.json', 'r') as f:
                data = json.load(f)
                games = data[member]['games-ranked']
            master += games
            i+=1
        master = list(set(master))
        return master

    async def max_games(self, ctx, pings):
        i = 0
        max = 0
        while i<len(ctx.message.mentions):
            member = str(ctx.message.mentions[i])
            with open('games2.json', 'r') as f:
                data = json.load(f)
                games = data[member]['games-ranked']
            if (len(games)>max):
                max = len(games)
            i+=1
        return max

    async def formatR(self, input):
        result = []
        for x in input:
            tmp = [0, x]
            result.append(tmp)
        return result

    async def compute_list(self, ctx, pings, max):
        i = 0
        master_games = await self.mastergames_list(ctx, pings)
        result = await self.formatR(master_games)
        while i<len(ctx.message.mentions):
            member = str(ctx.message.mentions[i])
            with open('games2.json', 'r') as f:
                data = json.load(f)
            games = data[member]['games-ranked']
            for x in master_games:
                if (games.count(x)==1):
                    rank = max - games.index(x)
                else:
                    rank = 0
                for y in result:
                    if (y[1]==x):
                        y[0]+=rank
                        break
            i += 1
        result.sort(key=lambda x: int(x[0]))
        return result

        

def setup(client):
    client.add_cog(gGames(client))
