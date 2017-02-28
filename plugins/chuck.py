import asyncio
import urllib.request
import json

from dev.plugin import *

async def chuckHandler(client, message):
	with urllib.request.urlopen('http://api.icndb.com/jokes/random') as f:
	    chuck = f.read().decode('utf-8')
	    asJson = json.loads(chuck)
	    await client.send_message(message.channel, asJson['value']['joke'])

plugin = Plugin("Chuck plugin", "Tells a random Chuck Norris joke.")
plugin.addHandler(CommandHandler("!chuck", chuckHandler, "!chuck - Tells you a random Chuck Norris joke."))