import asyncio
import json
import urllib.request

from dev.plugin import *

async def jokeHandler(client, message):
    joke = urllib.request.Request('https://icanhazdadjoke.com/')
    joke.add_header('Accept', 'application/json')
    dadjoke = urllib.request.urlopen(joke).read().decode('utf-8')
    asJson = json.loads(dadjoke)
    await client.send_message(message.channel, asJson['joke'])

plugin = Plugin("Joke plugin", "Tells a random joke")
plugin.addHandler(CommandHandler("!joke", jokeHandler, "!joke - Tells a random joke"))