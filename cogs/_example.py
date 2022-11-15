import discord
from discord.ext import commands
from cogs.extraclasses.jason import *
from cogs.extraclasses.perms import *

botData = FetchBotData()
serverData = FetchServerData()

class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Test processes active.")

    @commands.command()
    @commands.check(is_it_me)
    async def test(self, ctx):
        await ctx.send('Test extension cog works!')

def setup(bot):
    bot.add_cog(Test(bot))
