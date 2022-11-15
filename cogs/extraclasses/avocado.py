import os

def Avocado():
    for filename in os.listdir('./data'):
        if filename == 'avocadopog.png':
            return True