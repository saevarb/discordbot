import asyncio
import json
import urllib.request
 
from dev.plugin import *

async def yoMommaHandler(client, message):
    with urllib.request.urlopen('http://api.yomomma.info/') as f:
        momma = f.read().decode('utf-8')
        asJson = json.loads(momma)
        await client.send_message(message.channel, asJson['joke'])

plugin = Plugin("YoMomma plugin", "Tells your momma jokes")
plugin.addHandler(CommandHandler("!yoMomma", yoMommaHandler, "!yoMomma - Tells a random your momma jokes."))
