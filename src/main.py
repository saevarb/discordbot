import discord
import asyncio
import urllib.request
import logging
import json
import importlib.util
import glob
import discord.opus
from dev.plugin import loadPlugins

client = discord.Client()
client.plugins = loadPlugins()
# TODO: Necessary?
# discord.opus.load_opus()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    for plugin in client.plugins.values():
        await plugin.runPlugin(client, message)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

with open('.token.secret') as f:
    token = f.readline()
    client.run(token)
