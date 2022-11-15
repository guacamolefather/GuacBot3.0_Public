import discord
from discord.ext import commands
from cogs.extraclasses.read import *
from translate import Translator
from cogs.extraclasses.perms import *

class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Utility processes active.")

    @commands.command()
    @commands.check(is_it_me)
    async def utilitytest(self, ctx):
        await ctx.send('Utility extension cog works!')

    @commands.command()
    @commands.check(is_it_me)
    async def ping(self, ctx):
        await ctx.send('Latency: ' + str(round(self.bot.latency * 1000)) + 'ms.')

    @commands.command()
    async def avatar(self, ctx, *,  member : discord.Member=None):
        if (member == None):
            member = ctx.message.author
        memberAvatarUrl = member.avatar_url
        await ctx.send(memberAvatarUrl)
    
    @commands.command()
    async def emojiimage(self, ctx, *, msg):
        if not msg.startswith("<"):
            await ctx.send("Just an emoji, pls.")
            return
        
        try:
            _id = msg.split(":") # split by ":"
            if "<a" == _id[0]: # animated emojis structure <a:name:id>
                ext = "gif"
            else:
                ext = "png" # normal emojis structure <name:id>
            e_id = _id[2].split(">")[0].strip()# get the id
            # url for a emoji is like this
            url = f"https://cdn.discordapp.com/emojis/{e_id}.{ext}"

            await ctx.send(f"**Name**: :{_id[1]}: **Link**: {url}")
            
        except:
            await ctx.send("Just an emoji, pls.")
    
    @commands.command(aliases=["rolecall","attendence"])
    async def count(self, ctx):
        notbots = 0
        #withrole = 0
        online = 0
        icon_url = ctx.guild.icon_url
        embed = discord.Embed(title="Rolecall", description=f"{ctx.guild.member_count} members including me :)")
        embed.set_thumbnail(url=icon_url)

        #not bot members
        for member in ctx.guild.members:
            if not member.bot:
                notbots += 1
        embed.add_field(name='"Human" Member(s):',value=notbots, inline=False)

        #members in roles
        #for role in ctx.guild.roles:
            #for member in ctx.guild.members:
                #if role in member.roles:
                    #withrole += 1
            #embed.add_field(name=f"{role} members:",value=withrole, inline=False)
            #withrole = 0
        
        #online members
        for member in ctx.guild.members:
            if (str(member.status) == "online" or str(member.status) == "dnd") and not member.bot:
                online += 1
        embed.add_field(name='"Human" Member(s) Online/DND:',value=online, inline=False)

        await ctx.send(embed=embed)
        
    @commands.command()
    async def profile(self, ctx): #, *, member : discord.Member=None):
        #if (member == None):
        member = ctx.message.author
        embed = discord.Embed(title=str(member), description="Member's statistics:", colour=member.top_role.color, url="https://www.youtube.com/watch?v=iik25wqIuFo")
        embed.set_thumbnail(url=member.avatar_url)

        #Member's roles:
        member_roles = []
        fancy_roles_list = ""
        if (len(member.roles) > 1):
            raw_list = [role.mention for role in member.roles]
            raw_list.pop(0)
            for i in raw_list:
                member_roles.insert(0, i)
            for role in member_roles:
                fancy_roles_list = fancy_roles_list + "- " + role + "\n"
        else:
            fancy_roles_list = "None"
        embed.add_field(name="Role(s):",value=fancy_roles_list, inline=False)
        
        #How many channels member has access to:
        counter = 0
        for channel in ctx.guild.text_channels:
            if (channel.permissions_for(member).read_messages):
                counter = counter + 1
        embed.add_field(name="Channels:",value="Has access to " + str(counter) + " channels.",inline=False)

        embed.add_field(name="Messages sent:", value="at least 2?", inline=False)

        embed.add_field(name="Regular profile",value="This is the regular profile command. For the admin command, use $adminprofile (with admin priviledges).", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def reactions(self, ctx):
        triggers = ReadTriggers()
        fancyList = ""
        for i in triggers:
            if not isinstance(i, str):
                if fancyList.endswith(", "):
                    fancyList = fancyList + "("
                else:
                    fancyList = fancyList + ", ("
                for subtrigger in i:
                    if fancyList.endswith("("):
                        fancyList = fancyList + subtrigger
                    else:
                        fancyList = fancyList + ", " + subtrigger
                fancyList = fancyList + "), "
            else:
                if i == "409445517509001216":
                    fancyList = "@thememesareallreal"
                else:
                    if fancyList.endswith(", "):
                        fancyList = fancyList + i
                    else:
                        fancyList = fancyList + ", " + i
        await ctx.send(fancyList)
    
    @commands.command()
    async def translate(self, ctx, language, *, words):
        if("-" in language):
            translator= Translator(to_lang=language.split("-")[0], from_lang=language.split("-")[1])
        else:
            translator= Translator(to_lang=language)

        translated = translator.translate(words)

        await ctx.send(translated)

def setup(bot):
    bot.add_cog(Utility(bot))
