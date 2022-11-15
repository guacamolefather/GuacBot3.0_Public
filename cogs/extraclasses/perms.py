import discord
from cogs.extraclasses.jason import *

botData = FetchBotData()
serverData = FetchServerData()

async def not_blacklisted(ctx):
    botData = FetchBotData()
    serverData = FetchServerData()
    toreturn = ctx.author.id not in botData["Reactions"]["global_blacklist"] and ctx.guild.id not in botData["Reactions"]["server_blacklist"] and ctx.author.id not in serverData[str(ctx.guild.id)]["Commands"]["blacklist"]

    #if not toreturn:
        #await ctx.send("Sorry, you're blacklisted...")
    return toreturn

async def is_it_me(ctx):
    toreturn = ctx.author.id == 409445517509001216

    #if not toreturn:
        #await ctx.send("Sorry, that command is only for dad.")
    return toreturn

async def admin(ctx):
    if (ctx.author.guild_permissions.manage_guild):
        return True
    serverData = FetchServerData()
    for role in serverData[str(ctx.guild.id)]["HQ"]["adminroles"]:
        if role in ctx.author.roles:
            return True
    toreturn = ctx.author.id == 409445517509001216
    
    #if not toreturn:
        #await ctx.send("Sorry, that command is only for admins.")
    return toreturn

async def sophie(ctx):
    toreturn = True
    if (ctx.author.guild.id == 763550505469083650):
        toreturn = is_it_me or ctx.author.id == 562372596008484875

    #if not toreturn:
        #await ctx.send("Sorry, that command is only for Sophie...")
    return toreturn

async def test(ctx):
    await ctx.send("This is a thing...")
    return False