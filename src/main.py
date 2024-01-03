import discord
from discord.ext import commands
import time
import llama2
import threading
import asyncio
import json

conf = json.load(open("./system/settings.json"))["Discord"]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
message_que = []

def message_handler():
    global message_que
    while True:
        if len(message_que) > 0:
            message = message_que[0]
            response = llama2.respond(message)
            asyncio.run_coroutine_threadsafe(message.channel.send(response), bot.loop)
            message_que = message_que[1:]

        else:
            time.sleep(0.1)

def command(message):
    command = str(message.content)[1:]
    if command == "wipe":
        llama2.delete_context(message.author.id)
        return "Your chat-history was deletet of the server."

    elif command == "help":
        return open("./templates/help.md", "r").read()

    elif command == "undo":
        last_message = llama2.undo(message.author.id)
        return f"Message undone, your last message now is:\n```\n{last_message}\n```"

    else:
        return "Command not known."

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if (not message.author.bot == True):
        if isinstance(message.channel, discord.channel.DMChannel):
            message_content = str(message.content)
            if message_content[0] == "!":
                await message.channel.send(command(message))

            else:
                global message_que
                message_que.append(message)
        else:
            pass

threading._start_new_thread(message_handler, ())
bot.run(conf["API-Key"])