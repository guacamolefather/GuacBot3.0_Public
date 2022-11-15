import discord
from discord.ext import commands
import time
import requests
from cogs.extraclasses.jason import *
from cogs.extraclasses.perms import *

botData = FetchBotData()
serverData = FetchServerData()

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin processes active.")

    @commands.command()
    @commands.check(is_it_me)
    async def admintest(self, ctx):
        await ctx.send('Admin extension cog works!')

    @commands.command(aliases=['purge', 'prune', 'delete'])
    @commands.check(admin)
    async def clear(self, ctx, amount=1):
        time.sleep(1)
        await ctx.channel.purge(limit=amount+1)

    @commands.command()
    @commands.check(admin)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await ctx.send(f'Kicked {member.mention}.\nReason: {reason}.')
        await member.kick(reason=reason)

    @commands.command()
    @commands.check(admin)
    async def ban(self, ctx, member : discord.Member, *, reason="A good one, trust me."):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention}.\nReason: {reason}.')

    @commands.command()
    @commands.check(admin)
    async def softban(self, ctx, member : discord.Member, *, reason="A good one, trust me."):
        await member.ban(reason=reason)
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Softbanned {member.mention}.\nReason: {reason}.')
                return

    @commands.command()
    @commands.check(admin)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {member.mention}.')
                return

    @commands.command()
    @commands.check(admin)
    async def giverole(self, ctx, role: discord.Role, member: discord.Member):
        await member.add_roles(role)
        await ctx.send(f'Given {role.mention} to {member.mention}.')

    @commands.command()
    @commands.check(admin)
    async def takerole(self, ctx, role: discord.Role, member: discord.Member):
        await member.remove_roles(role)
        await ctx.send(f'Taken {role.mention} from {member.mention}.')

    @commands.command()
    @commands.check(admin)
    async def customemoji(self, ctx, *, emoji_name=None):
        attached = ctx.message.attachments
        
        if ctx.message.reference != None and attached == []:
            original = await ctx.fetch_message(id=ctx.message.reference.message_id)
            if original.attachments != None:
                attached = original.attachments
            if original.embeds != None and attached == []:
                img_data = requests.get(original.embeds[0].url).content
                if (emoji_name == None):
                    emoji_name = "stolenemoji"
                await ctx.guild.create_custom_emoji(name=emoji_name, image=img_data)
                await ctx.send("Done!")
                return

        if (len(attached) < 1):
            await ctx.send("You need to attach or reply to an image.")
        else:
            emoji = attached[0]
            emoji_bytes = await emoji.read()
            if emoji_name == None:
                name, filetype = emoji.filename.split(".")
                if (len(name) < 33):
                    emoji_name = name
                else:
                    emoji_name = name[0:32]
            await ctx.guild.create_custom_emoji(name=emoji_name, image=emoji_bytes)
            await ctx.send("Done!")
    
    
    @customemoji.error
    async def customemoji_error(ctx, error):
        if isinstance(error, discord.HTTPException):
            await ctx.send('Something went wrong...')
    
    
    @commands.command()
    @commands.check(admin)
    async def stealemoji(self, ctx, *, msg):

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

            img_data = requests.get(url).content
            emoji_name = _id[1]

            await ctx.guild.create_custom_emoji(name=emoji_name, image=img_data)
            await ctx.send("Done!")
            
        except Exception as e:
            if not isinstance(e, discord.Forbidden):
                await ctx.send(f"Just an emoji, pls.")
            else:
                await ctx.send(f"I don't have permission to do that...")

    @commands.command()
    @commands.check(admin)
    async def adminprofile(self, ctx, *, member : discord.Member=None):
        if (member == None):
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

        #Member's permissions:
        member_permissions_str = []
        member_permissions_bool = []
        fancy_permissions_list = ""
        for permission in member.guild_permissions:
            permission_name, permission_bool = str(permission).split(",")
            member_permissions_str.append(permission_name)
            member_permissions_bool.append(permission_bool)
        i = 0
        for permission_name in member_permissions_str:
            fancy_permissions_list = fancy_permissions_list + "- " + permission_name + ": " + member_permissions_bool[i] + "\n"
            i = i + 1
        forbidden = "()'"
        for char in fancy_permissions_list: 
            if char in forbidden: 
                fancy_permissions_list = fancy_permissions_list.replace(char, "")
        forbidden = "_"
        for char in fancy_permissions_list: 
            if char in forbidden: 
                fancy_permissions_list = fancy_permissions_list.replace(char, " ")
        embed.add_field(name="Server Permissions:",value=fancy_permissions_list,inline=False)

        #How many channels member has access to:
        channel_names = []
        for channel in ctx.guild.text_channels:
            if (channel.permissions_for(member).read_messages):
                channel_names.append(str(channel))
        fancy_channels_list = ""
        for room in channel_names:
            fancy_channels_list = fancy_channels_list + "- " + room + "\n"
        embed.add_field(name="Accessible channels:",value=fancy_channels_list,inline=False)

        embed.add_field(name="Admin profile",value="This is the admin-level profile command.",inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(admin)
    async def rolecount(self, ctx):
        withrole = 0
        memberswithrole = ""
        fields = 1

        icon_url = ctx.guild.icon_url
        embed = discord.Embed(title="Role Count", description=f"{ctx.guild.member_count} members including me :)",color=ctx.guild.owner.top_role.color)
        embed.set_thumbnail(url=icon_url)
        
        for role in ctx.guild.roles:
            for member in ctx.guild.members:
                if role in member.roles:
                    withrole += 1
                    memberswithrole += " - " + member.display_name
            print(len(memberswithrole))
            fields += 1
            
            embed.add_field(name=f"{role} members:",value=str(withrole) + ": (" + memberswithrole + ")", inline=False)
            withrole = 0
            memberswithrole = ""
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Admin(bot))
