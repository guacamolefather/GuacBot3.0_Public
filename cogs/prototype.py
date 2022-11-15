import discord
from discord.ext import commands
from cogs.extraclasses.perms import *


def charLimit(longString):
    if (len(longString) > 2000):
        substringList = []
        loops = (int) (len(longString) / 2000)
        x = 0
        for i in range(loops + 1):
            substringList.append(longString[x:x + 2000])
            x = x + 2000
        return substringList
    else:
        return [longString]

class Prototype(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Prototype processes active.')

    @commands.command()
    @commands.check(is_it_me)
    async def prototypetest(self, ctx):
        await ctx.send('Prototype extension cog works!')
        
def setup(bot):
    bot.add_cog(Prototype(bot))
