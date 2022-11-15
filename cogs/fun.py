import discord
from discord.ext import commands
import random
from cogs.extraclasses.perms import *

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun processes active.")

    @commands.command()
    @commands.check(is_it_me)
    async def funtest(self, ctx):
        await ctx.send('Fun extension cog works!')

    @commands.command(aliases=['8ball'])
    async def eightball(self, ctx, *, question="TBD (Try typing a question after the command)"):
        responses = ['Hmmmm.',
                     'Ask again.',
                     "It's possible.",
                     'Maybe.',
                     'Perhaps.',
                     'Not sure.',
                     'Uncertain.',
                     '(͡° ͜ʖ ͡°)',
                     'No clue.',
                     'Response hazy.']
        if ctx.author.id != 689511753318531081:
            await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
        else:
            await ctx.send("Yes.")

    @commands.command(aliases=['rd', 'diceroll'])
    async def rolldice(self, ctx, sides=6, amount=1):
        diceList=[]
        for i in range(0, amount):
            diceList.append(random.randint(1,sides))
            i = i + 1
        await ctx.send("Your roll(s) are:  " + str(diceList))

    @commands.command()
    async def snap(self, ctx):
        snap = random.randint(0, 1)
        if snap == 0:
            await ctx.send("You survived, now go make use of the resources you have left and rebuild your world.")
        if snap == 1:
            await ctx.send("Sorry, little one, but you were sacrificed for the greater good.")

    @commands.command()
    async def rps(self, ctx, choice=""):
        botchoice = random.randint(0, 2)
        if botchoice == 0 and choice.lower() == "rock":
            await ctx.send("I chose rock!  It's a tie!")
        elif botchoice == 0 and choice.lower() == "paper":
            await ctx.send("I chose rock! You win!")
        elif botchoice == 0 and choice.lower() == "scissors":
            await ctx.send("I chose rock! I win!")
        elif botchoice == 1 and choice.lower() == "rock":
            await ctx.send("I chose paper!  I win!")
        elif botchoice == 1 and choice.lower() == "paper":
            await ctx.send("I chose paper! It's a tie!")
        elif botchoice == 1 and choice.lower() == "scissors":
            await ctx.send("I chose paper! You win!")
        elif botchoice == 2 and choice.lower() == "rock":
            await ctx.send("I chose scissors!  You win!")
        elif botchoice == 2 and choice.lower() == "paper":
            await ctx.send("I chose scissors! I win!")
        elif botchoice == 2 and choice.lower() == "scissors":
            await ctx.send("I chose scissors! It's a tie!")
        else:
            if botchoice == 0:
                await ctx.send("I chose rock!")
            elif botchoice == 1:
                await ctx.send("I chose paper!")
            elif botchoice == 2:
                await ctx.send("I chose scissors!")
            else:
                await ctx.send("You've royally screwed up")

    @commands.command(aliases=['bn'])
    async def bignumber(self, ctx):
        for i in range(0, random.randint(1, 1000)):
            i = i * random.randint(1, 1000)
        await ctx.send(i)

    @commands.command(aliases=['brn'])
    async def biggernumber(self, ctx):
        for i in range(1000, random.randint(1001, 1000000)):
            i = i * random.randint(1000, 1000000)
        await ctx.send(i)

    @commands.command(aliases=['bstn'])
    async def biggestnumber(self, ctx):
        for i in range(0, random.randint(1, 1000)):
            i = i ** random.randint(1, 1000)
        await ctx.send(i)

    @commands.command(hidden=True)
    async def secret(self, ctx):
        await ctx.channel.purge(limit=1)
        await ctx.send("SHH!!!", delete_after=3)
    
    #https://www.countryliving.com/life/a27452412/best-dad-jokes/
    @commands.command(aliases=['joke'])
    async def dadjoke(self, ctx):
        jokes = ["I'm afraid for the calendar. Its days are numbered.",
        "My wife said I should do lunges to stay in shape. That would be a big step forward.",
        "Singing in the shower is fun until you get soap in your mouth. Then it's a soap opera.",
        "I thought the dryer was shrinking my clothes. Turns out it was the refrigerator all along.",
        "Dear Math, grow up and solve your own problems.",
        "Have you heard about the chocolate record player? It sounds pretty sweet.",
        "I only know 25 letters of the alphabet. I don't know y.",
        "A skeleton walks into a bar and says, 'Hey, bartender. I'll have one beer and a mop.'",
        "I asked my dog what's two minus two. He said nothing.",
        "I don't trust those trees. They seem kind of shady.",
        "My wife is really mad at the fact that I have no sense of direction. So I packed up my stuff and right!",
        "I don't trust stairs. They're always up to something."]
        i = len(jokes) - 1
        jokechoice = random.randint(0, i)
        await ctx.send(jokes[jokechoice])

    #https://minecraft.fandom.com/wiki/Death_messages
    @commands.command()
    @commands.check(sophie)
    async def kill(self, ctx, member : discord.Member):
        if member.id == ctx.author.id:
            await ctx.send("Do you need a lighthouse??")
            return
        if member.id == 409445517509001216 and random.randint(1, 10) != 8:
            await ctx.send("Dad can't be killed??")
            return
        if member.id == 582337819532460063:
            await ctx.send("Please don't kill me...")
            return
        dead = member.display_name
        killer = ctx.author.display_name
        deaths = [f"{dead} was shot.",
        f"{dead} blew themselves up!",
        f"{dead} fell to their death...",
        f"{dead} was pummeled by {killer}.",
        f"{dead} was pricked to death via cactus!",
        f"{dead} drowned...",
        f"{dead} experienced kinetic energy...",
        f"{dead} went up in flames!",
        f"{dead} was impaled!",
        f"{dead} was squashed by {killer}...",
        f"{dead} went out with a bang!",
        f"{dead} tried to swim in lava...",
        f"{dead} discovered the floor was lava!",
        f"{dead} was struck by lightning!",
        f"{dead} froze to death...",
        f"{dead} was slain by {killer}!",
        f"{dead} took the L.",
        f"{killer} handed {dead} the L."]
        i = len(deaths) - 1
        deathchoice = random.randint(0, i)
        await ctx.send(deaths[deathchoice])

def setup(bot):
    bot.add_cog(Fun(bot))
