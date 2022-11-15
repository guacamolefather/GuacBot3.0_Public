import discord
from cogs.extraclasses.perms import *
from cogs.extraclasses.read import *
from cogs.extraclasses.jason import *
import random
import time

#Version 3.0 experimental

client = discord.Client()

botData = FetchBotData()
serverData = FetchServerData()

def charLimit(index, responsesList):
    reactionMessage = responsesList[index]
    if (len(reactionMessage) > 2000):
        substringList = []
        loops = (int) (len(reactionMessage) / 2000)
        x = 0
        for i in range(loops + 1):
            substringList.append(reactionMessage[x:x + 2000])
            x = x + 2000
        return substringList
    else:
        return [responsesList[index]]

@client.event
async def on_ready():
    print('Reactions active.')

@client.event
async def on_message(message):
    botData = FetchBotData()
    serverData = FetchServerData()

    if message.author == client.user:
        return
    if random.randint(1, 3) != 3:
        return
    try:
        if not serverData[str(message.guild.id)]["Reactions"]["reactions"]:
            return
        if message.author.bot and not serverData[str(message.guild.id)]["Reactions"]["botreactions"]:
            return
        if message.guild.id in botData["Reactions"]["server_blacklist"] or message.author.id in serverData[str(message.guild.id)]["Reactions"]["blacklist"]:
            return
    except:
        pass
    if message.author.id in botData["Reactions"]["global_blacklist"]:
        return
    if "not now, guac" == message.content.lower() and message.author.id == 409445517509001216:
        botData["Reactions"]["wait_until"] = time.time() + 300.0
        UpdateBotData(botData)
        await message.channel.send("Sorry, I'll be back in five...")
        return
    if botData["Reactions"]["wait_until"] > time.time():
        return
    if client.user.mentioned_in(message) and message.reference is None:
        await message.channel.send("Use $help in a channel I can send messages in, use $invite to invite me to your own server, or use this link to join the support server: https://discord.gg/mJpg2DBM6D")
        return
    if "guacbot" in message.content.lower() or "guac" in message.content.lower() or "guacy" in message.content.lower() or "guaccy" in message.content.lower() or "guacity" in message.content.lower() or "son" in message.content.lower():
        return
    
    triggersList = ReadTriggers()
    responsesList = ReadResponses()

    punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
    unPuncMessage = message.content.lower()
    for char in unPuncMessage: 
        if char in punc:
            unPuncMessage = unPuncMessage.replace(char, " ") 
    for trigger in triggersList:
        if not isinstance(trigger, str):
            for subtrigger in trigger:
                if Conditional(unPuncMessage, subtrigger):
                    reaction = charLimit(triggersList.index(trigger), responsesList)
                    for i in reaction:
                        if "\\n" in i:
                            i = i.replace("\\n", "\n")
                        await message.channel.send(str(i))
        else:
            if Conditional(unPuncMessage, trigger):
                reaction = charLimit(triggersList.index(trigger), responsesList)
                for i in reaction:
                    if "\\n" in i:
                        i = i.replace("\\n", "\n")
                    await message.channel.send(str(i))

    #Conditional(fullMessage, trigger)

    #Special
    if "i’m " in message.content.lower():
        if "I’m" in message.content:
            await message.channel.send('Hello "' + message.content.split("I’m ")[1] + '", I\'m GuacBot!')
        else:
            await message.channel.send('Hello "' + message.content.split("i’m ")[1] + '", I\'m GuacBot!')

    #Special
    if "i'm " in message.content.lower():
        if "I'm" in message.content:
            await message.channel.send('Hello "' + message.content.split("I'm ")[1] + '", I\'m GuacBot!')
        else:
            await message.channel.send('Hello "' + message.content.split("i'm ")[1] + '", I\'m GuacBot!')

    #Special
    if " im " in message.content.lower():
        if "Im" in message.content:
            await message.channel.send('Hello "' + message.content.split("Im ")[1] + '", I\'m GuacBot!')
        else:
            await message.channel.send('Hello "' + message.content.split("im ")[1] + '", I\'m GuacBot!')

    #Special
    if "i am " in message.content.lower():
        if "I am" in message.content:
            await message.channel.send('Hello "' + message.content.split("I am ")[1] + '", I\'m GuacBot!')
        else:
            await message.channel.send('Hello "' + message.content.split("i am ")[1] + '", I\'m GuacBot!')

    #Special
    if "lmao" == unPuncMessage or "lmfao" == unPuncMessage:
        await message.channel.send(message.content)

    #Special
    if "what" == message.content.lower():
        finishers = ["...the heck?",
        "...in the world?",
        "...in the goddamn?",
        "...the hell?",
        "...is going on here?",
        "...are you on about?",
        "...is the quadratic formula?"]
        i = len(finishers) - 1
        finisherChoice = random.randint(0, i)
        await message.channel.send(finishers[finisherChoice])
        
    #Special
    if "what?" == message.content.lower():
        finishers = ["I have no idea.",
        "Beats me.",
        "Time to get a watch... wait.",
        "Wouldn't you like to know?"]
        i = len(finishers) - 1
        finisherChoice = random.randint(0, i)
        await message.channel.send(finishers[finisherChoice])
            
    #Special
    if "love you" in message.content.lower():
        if "i love you" in message.content.lower():
            await message.channel.send("I love you too, full homo")
        else:
            await message.channel.send("I love you too, no homo")

    #Special
    if "spanish" in message.content.lower():
        if random.randint(1,3) == 1:
            await message.channel.send("Nobody expects The Spanish Inquisition!")

    #Special
    if "micolash" in message.content.lower() or "kos" in message.content.lower() or "bloodborne" in message.content.lower():
        quotes = ["Ahh, Kos, or some say Kosm... Do you hear our prayers?",
        "No, we shall not abandon the dream.",
        "No one can catch us! No one can stop us now! *cackling*",
        "Ah hah hah ha! Ooh! Majestic! A hunter is a hunter, even in a dream. But, alas, not too fast! The nightmare swirls and churns unending!",
        "As you once did for the vacuous Rom, grant us eyes, grant us eyes. Plant eyes on our brains, to cleanse our beastly idiocy.",
        "The grand lake of mud, hidden now, from sight.",
        "The cosmos, of course!",
        "Let us sit about, and speak feverishly. Chatting into the wee hours of...",
        "Now I'm waking up, I'll forget everything...",
        "AAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHH"]
        i = len(quotes) - 1
        quotechoice = random.randint(0, i)
        await message.channel.send(quotes[quotechoice])

    #Special
    if "shakespeare" in message.content.lower():
        quotes = ["To be, or not to be: that is the question: Whether 'tis nobler in the mind to suffer The slings and arrows of outrageous fortune, Or to take arms against a sea of troubles, And by opposing end them. To die: to sleep...",
        "This above all: to thine own self be true, And it must follow, as the night the day, Thou canst not then be false to any man.",
        "Cowards die many times before their deaths; The valiant never taste of death but once.",
        "Men at some time are masters of their fates: The fault, dear Brutus, is not in our stars, But in ourselves, that we are underlings.",
        "What's in a name? That which we call a rose By any other word would smell as sweet...",
        "Good night, good night! Parting is such sweet sorrow, That I shall say good night till it be morrow.",
        "All the world's a stage, And all the men and women merely players: They have their exits and their entrances; And one man in his time plays many parts.",
        "The robbed that smiles, steals something from the thief.",
        "Uneasy lies the head that wears the crown.",
        "All that glitters is not gold."]
        i = len(quotes) - 1
        quotechoice = random.randint(0, i)
        await message.channel.send(quotes[quotechoice])

#~~~ End of if statements ~~~
client.run(botData["HQ"]["token"])
