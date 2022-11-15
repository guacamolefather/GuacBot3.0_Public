import random
import json
import discord
import time

import torch

from cogs.extraclasses.model import NeuralNet
from cogs.extraclasses.nltk_utils import bag_of_words, tokenize
from cogs.extraclasses.jason import *

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('data/intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

botData = FetchBotData()

client = discord.Client()

@client.event
async def on_ready():
    print("NLP active.")

@client.event
async def on_message(message):
    botData = FetchBotData()
    if message.author == client.user:
        return
    if message.author.bot == True:
        return
    if message.author.id in botData["Reactions"]["global_blacklist"] or message.guild.id in botData["Reactions"]["server_blacklist"]:
        return
    lowerMessage = message.content.lower()
    if "guacbot" in lowerMessage or "guac" in lowerMessage or "guacy" in lowerMessage or "guaccy" in lowerMessage or "guacity" in lowerMessage:
        name = lowerMessage.split("guac")[1]
        name = "guac" + name.split(" ")[0]
        name = tokenize(name)[0]
        await message.channel.send(interaction(name, lowerMessage))

def interaction(name, sentence):
    message = sentence
    sentence = tokenize(sentence)
    sentence.pop(sentence.index(name))
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return f"{random.choice(intent['responses'])}"
    else:
        if random.randint(1, 2) != 2:
            return
        else:
            responses = ["I do not understand...", "I don't get it?", "Huh?", f'Calling "{message}" on mobile?']
            return responses[random.randint(0,len(responses) - 1)]

client.run(botData["HQ"]["token"])
