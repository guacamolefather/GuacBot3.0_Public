import discord, time, os, subprocess, random
from discord.ext import commands, tasks, bridge
from cogs.extraclasses.timer import *
from cogs.extraclasses.jason import *
from cogs.extraclasses.avocado import *
from cogs.extraclasses.perms import *
from itertools import cycle

#Version 3.0 experimental
intents = discord.Intents.all()
bot = discord.ext.commands.Bot(command_prefix = '$', intents=intents, case_insensitive=True, activity=discord.Game("Only legends see this."))
bot.add_check(not_blacklisted)

@bot.event
async def on_ready():
    os.system('cls')
    print("Main bot processes active.")
    RefreshServerData(bot)
    change_status.start()

@bot.event
async def on_guild_join():
    RefreshServerData(bot)

@bot.event
async def on_guild_remove():
    RefreshServerData(bot)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That isn't a command, buddy.")
        return
    if isinstance(error, commands.CommandInvokeError):
        if isinstance(error.original, discord.Forbidden):
            await ctx.send("I don't have the permissions to do that here...")
            return
        else:
            await ctx.send_help(ctx.command)
    if isinstance(error, commands.CheckFailure):
        if (not await not_blacklisted(ctx)):
            await ctx.send("Sorry, you're blacklisted...")
        elif (not await is_it_me(ctx)):
            await ctx.send("Sorry, that command is only for dad.")
        elif (not await admin(ctx)):
            await ctx.send("Sorry, that command is only for admins.")
        elif (not await sophie(ctx)):
            await ctx.send("Sorry, that command is only for Sophie...")
        else:
            await ctx.send("Sorry, you don't have permission to do that...")
        return
    channel = await ctx.bot.fetch_channel(1037298707705634917)
    await channel.send(f"Error {type(error)} on command ${ctx.command}: {error}")

@bot.command()
@commands.check(is_it_me)
async def errorme(ctx):
    int("lmao")

@bot.command()
@commands.check(is_it_me)
async def refreshserverdata(ctx):
    RefreshServerData(bot)
    await ctx.send("Refreshing server data!")

@bot.command()
@commands.check(is_it_me)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'Extension "{extension}" loaded!')

@load.error
async def load_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please choose what cog to load.')
    else:
        channel = ctx.bot.fetch_channel(1037298707705634917)
        await channel.send(f"Error while loading cog: {error}")

@bot.command()
@commands.check(is_it_me)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Extension "{extension}" unloaded!')

@unload.error
async def unload_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please choose what cog to unload.')
    else:
        channel = ctx.bot.fetch_channel(1037298707705634917)
        await channel.send(f"Error while unloading cog: {error}")

@bot.command()
@commands.check(is_it_me)
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'Extension "{extension}" reloaded!')

@reload.error
async def reload_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please choose what cog to reload.')
    else:
        channel = ctx.bot.fetch_channel(1037298707705634917)
        await channel.send(f"Error while reloading cog: {error}")

@bot.command()
@commands.check(is_it_me)
async def die(ctx):
    await ctx.send("Goodbye, father.")
    await bot.change_presence(activity=discord.Game("Goodbye."))
    ta.kill()
    r.kill()
    nlp.kill()
    p.kill()
    os.system('cls')
    quit()

@die.error
async def die_error(ctx, error):
    channel = ctx.bot.fetch_channel(1037298707705634917)
    await channel.send(f"Error while dying: {error}")

@bot.command()
@commands.check(is_it_me)
async def restart(ctx):
    await ctx.send("Restarting!")
    subprocess.Popen(["python", "GuacBotHQ3.0.py"])
    ta.kill()
    r.kill()
    nlp.kill()
    p.kill()
    quit()

@restart.error
async def restart_error(ctx, error):
    channel = ctx.bot.fetch_channel(1037298707705634917)
    await channel.send(f"Error while restarting: {error}")

@bot.command(description="Displays my uptime and when it was last checked!")
async def uptime(ctx):
    time_elapsed = time.time() - botData["HQ"]["start_time"]
    time_checked = time.time() - botData["HQ"]["time_checked"]
    botData["HQ"]["time_checked"] = time.time()
    UpdateBotData(botData)
    await ctx.send("Uptime: " + time_convert(time_elapsed) + "\nLast Checked: " + time_convert(time_checked) + " ago.")

@uptime.error
async def uptime_error(ctx, error):
    await ctx.send(f"Error while checking uptime: {error}")

@bot.command(description="Guac will send you his link and a link to the support server!")
async def invite(ctx):
    await ctx.send("Link to bot: https://discord.com/api/oauth2/authorize?client_id=582337819532460063&permissions=8&scope=bot\nLink to support server: https://discord.gg/mJpg2DBM6D")

@bot.slash_command(description="Guac will send you his link and a link to the support server!")
async def invite(ctx):
    await ctx.respond("Link to bot: https://discord.com/api/oauth2/authorize?client_id=582337819532460063&permissions=8&scope=bot\nLink to support server: https://discord.gg/mJpg2DBM6D", ephemeral=True)

#Load cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename.startswith("_"):
        bot.load_extension(f'cogs.{filename[:-3]}')

#Load JSON file
botData = InitBotData()

#Status loop
def NewOrder():
    statusorder = []
    indices = list(random.sample(range(len(possiblestatuses)), len(possiblestatuses)))
    for i in indices:
        statusorder.append(possiblestatuses[i])
    return statusorder

possiblestatuses = botData["HQ"]["possible_statuses"]

status = cycle(NewOrder())
@tasks.loop(seconds=300)
async def change_status():
    newStatus = next(status)
    activityType = newStatus["type"]
    activityText = newStatus["status"]
    if activityType == "game":
        await bot.change_presence(activity=discord.Game(activityText))
    elif activityType == "stream":
        await bot.change_presence(activity=discord.Streaming(name=activityText, url="https://www.twitch.tv/thememesareallreal"))
    elif activityType == "watch":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activityText))
    elif activityType == "listen":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activityText))

#Open other GuacBot pieces
r = subprocess.Popen(["python", "GuacBotReaction3.0.py"])
ta = subprocess.Popen(["python", "GuacBotTerminalAnimation.py"])
nlp = subprocess.Popen(["python", "GuacBotNLP.py"])
p = subprocess.Popen(["python", "GuacBotPersonal.py"])

#Start bot with token in json file
if Avocado():
    bot.run(botData["HQ"]["token"])