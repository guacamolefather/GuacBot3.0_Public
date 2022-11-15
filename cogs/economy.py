import discord
from discord.ext import commands
from cogs.extraclasses.jason import *
from cogs.extraclasses.perms import *
import random

botData = FetchBotData()
serverData = FetchServerData()
bankData = FetchBankData()

class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Economy processes active.")

    @commands.command()
    @commands.check(is_it_me)
    async def economytest(self, ctx):
        await ctx.send('Economy extension cog works!')
    
    @commands.command()
    async def balance(self, ctx):
        HasBankAccount(ctx.message.author)
        bankData = FetchBankData()

        bankBalance = bankData["accounts"][str(ctx.message.author.id)]["bank"]["balance"]
        wallet = bankData["accounts"][str(ctx.message.author.id)]["wallet"]
        await ctx.send(f"Your bank balance is ${bankBalance} and there is ${wallet} in your wallet.")

    @commands.command()
    async def beg(self, ctx):
        HasBankAccount(ctx.message.author)
        bankData = FetchBankData()

        if random.randint(1, 4) == 3:
            luck = random.randint(1, 100)
            change = 0
            if luck == 1:
                change = -5
            elif luck < 10:
                change = 1
            elif luck < 40:
                change = 5
            elif luck < 75:
                change = 10
            elif luck < 100:
                change = 20
            else:
                change = 50

            wallet = bankData["accounts"][str(ctx.message.author.id)]["wallet"]
            bankData["accounts"][str(ctx.message.author.id)]["wallet"] = wallet + change
            UpdateBankData(bankData)
            if change >= 0:
                await ctx.send(f"Fine, here's ${change}, you now have ${wallet + change} in your wallet...")
            else:
                await ctx.send(f"How about you give me some money instead?? I'm taking ${change * -1}, you now have ${wallet + change} in your wallet!")
        else:
            await ctx.send("No.")

    @commands.command(aliases=["gamble"])
    async def luckgamble(self, ctx, amount=5):
        HasBankAccount(ctx.message.author)
        bankData = FetchBankData()

        wallet = bankData["accounts"][str(ctx.message.author.id)]["wallet"]
        try:
            togamble = int(amount)
            if togamble > wallet:
                await ctx.send(f"You don't own that much money, you have ${wallet} in your wallet!")
                return

            wallet = wallet - togamble

            luck = random.randint(1, 100)
            if luck < 35:
                togamble = 0
            elif luck < 65:
                togamble = togamble
            elif luck < 100:
                togamble = togamble * 2
            else:
                togamble = togamble * 3
            
            bankData["accounts"][str(ctx.message.author.id)]["wallet"] = wallet + togamble
            UpdateBankData(bankData)
            wallet = bankData["accounts"][str(ctx.message.author.id)]["wallet"]

            if togamble == 0:
                await ctx.send(f"Oops, you lost your money... You now have ${wallet}")
            elif togamble == int(amount):
                await ctx.send(f"You broke even... You still have ${wallet}")
            else:
                await ctx.send(f"You multipled your amount by {togamble / int(amount)}! You now have ${wallet}!")

        except:
            await ctx.send("Something went wrong... Make sure you put in an amount you own!")

    @commands.command()
    async def guessgamble(self, ctx, *, amountguess="5 0"):
        HasBankAccount(ctx.message.author)
        bankData = FetchBankData()

        wallet = bankData["accounts"][str(ctx.message.author.id)]["wallet"]
        try:
            amount, guess = amountguess.split(" ")
            togamble = int(amount)
            guess = int(guess)

            if togamble > wallet:
                await ctx.send(f"You don't own that much money, you have ${wallet} in your wallet!")
                return
            if guess < 1 or guess > 100:
                await ctx.send("Please make a guess between 1 and 100 (inclusive) after your amount.")
                return

            wallet = wallet - togamble

            luck = random.randint(1, 100)
            if abs(guess - luck) >= 35:
                togamble = 0
            elif abs(guess - luck) >= 20:
                togamble = togamble
            elif abs(guess - luck) > 0:
                togamble = togamble * 2
            else:
                togamble = togamble * 3
            
            bankData["accounts"][str(ctx.message.author.id)]["wallet"] = wallet + togamble
            UpdateBankData(bankData)
            wallet = bankData["accounts"][str(ctx.message.author.id)]["wallet"]

            if togamble == 0:
                await ctx.send(f"Oops, your guess ({guess}) was {abs(guess - luck)} away from my guess, {luck}. You went 35 or over, so you lost your money... You now have ${wallet}")
            elif togamble == int(amount):
                await ctx.send(f"Your guess ({guess}) was {abs(guess - luck)} away from my guess, {luck}. You went 20 or over but under 35, so you broke even... You still have ${wallet}")
            else:
                await ctx.send(f"Your guess ({guess}) was {abs(guess - luck)} away from my guess, {luck}. You were under 20 away, so you multipled your amount by {togamble / int(amount)}! You now have ${wallet}!")

        except Exception as e:
            if type(e) == ValueError:
                await ctx.send("Make you sure send your amount THEN a guess between 1 and 100 separated by a space.")
            else:
                await ctx.send(f"Something went wrong... {e}")

def setup(bot):
    bot.add_cog(Economy(bot))
