import discord
from discord.ext import commands
from cogs.extraclasses.read import *
from cogs.extraclasses.jason import *
from cogs.extraclasses.perms import *

botData = FetchBotData()
serverData = FetchServerData()

class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Owner processes active.")

    @commands.command()
    @commands.check(is_it_me)
    async def ownertest(self, ctx):
        await ctx.send('Owner extension cog works!')

    @commands.command(aliases=['echo'])
    @commands.check(is_it_me)
    async def say(self, ctx, *, words: commands.clean_content):
        print(words)
        await ctx.channel.purge(limit=1)
        await ctx.send(words)
    
    @commands.command()
    @commands.check(is_it_me)
    async def tts(self, ctx, *, words: commands.clean_content):
        await ctx.channel.purge(limit=1)
        await ctx.send(words, tts=True)
        
    @commands.command()
    @commands.check(is_it_me)
    async def changestatus(self, ctx, *, status):
        # Setting "Listening" status
        if "listen" in status.lower():
            listenStatus = status.replace("listen ", "")
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=listenStatus))

        # Setting "Watching" status
        elif "watch" in status.lower():
            watchStatus = status.replace("watch ", "")
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=watchStatus))

        # Setting "Streaming" status
        elif "stream" in status.lower():
            streamStatus = status.replace("stream ", "")
            await self.bot.change_presence(activity=discord.Streaming(name=streamStatus, url="https://www.twitch.tv/thememesareallreal"))

        # Setting broken custom status
        elif "custom" in status.lower():
            customStatus = status.replace("custom ", "")
            await self.bot.change_presence(activity=discord.CustomActivity(name=customStatus))
            
        # Setting "Playing" status
        else:
            await self.bot.change_presence(activity=discord.Game(status))

        await ctx.send("Status changed!")

    @commands.command()
    @commands.check(is_it_me)
    async def globalblacklist(self, ctx, member : discord.Member):
        botData["Reactions"]["global_blacklist"].append(member.id)
        UpdateBotData(botData)
        await ctx.send(f"{member.display_name} now on Guac global blacklist.")

    @commands.command()
    @commands.check(is_it_me)
    async def globalunblacklist(self, ctx, *, member : discord.Member):
        indexingPurposes = botData["Reactions"]["global_blacklist"]
        botData["Reactions"]["global_blacklist"].pop(indexingPurposes.index(member.id))
        UpdateBotData(botData)
        await ctx.send(f"{member.display_name} bailed from Guac global blacklist :rolling_eyes:")

    @commands.command()
    @commands.check(is_it_me)
    async def readblacklist(self, ctx):
        await ctx.send(botData["Reactions"]["global_blacklist"])

    @commands.command()
    @commands.check(is_it_me)
    async def allguilddata(self, ctx):
        await ctx.send(serverData)

def setup(bot):
    bot.add_cog(Owner(bot))