import discord
import os
from dotenv import load_dotenv
import asyncio
import pymongo
from pymongo import MongoClient
from chess_game import MyBoard

import random

#load contents of the .env file as environment variables
load_dotenv()
URI = os.getenv('MONGO_URI')
TOKEN = os.getenv("DISCORD_TOKEN")

board = MyBoard()

#connect to the databse
client = MongoClient(URI)
db = client["CaptureTheFlag"]
collection = db["Game"]

#set intents for discord client
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

#create instance of a client (connects to discord)
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'logged in as {client.user} (ID:{client.user.id}) on server: {client.guilds[0]}')
    print(f'intents: {intents}')
    print("-----")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send(f'Hello, {message.author}')

    if message.content.startswith('$guess'):
        await message.channel.send(f'Guess a number between 1 and 10')

        def correct(m):
            return m.author == message.author and m.content.isdigit()
        
        answer = random.randint(1,10)

        try:
            guess = await client.wait_for('message', check=correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await message.channel.send(f'sorry, you took too long. the answer was {answer}')
        
        if int(guess.content) == answer:
            await message.channel.send('Correct!')
        elif int(guess.content) > answer:
            await message.channel.send('Too high.')
        else:
            await message.channel.send('Too low.')

    if message.content.startswith(";chess"):
        await message.channel.send("Let's play chess! :smile:")
        await message.channel.send(board.unicode(invert_color=True))
    
    elif message.content.startswith(";fen"):
        await message.channel.send(board.fen())

    elif(message.content.startswith(";")):
        move = message.content.strip(";")
        result = board.move(move)
        if not result:
            await message.channel.send(board.unicode(invert_color=True))
        else:
            await message.channel.send(result)




client.run(TOKEN)