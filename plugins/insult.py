import asyncio
import urllib.request
 
from dev.plugin import *

async def insultHandler(client, message):
    hasTarget = len(message.content.split()) > 1
    if hasTarget:
        targets = message.mentions
        insults = []
        await client.send_typing(message.channel)
        for target in message.mentions:
            # print('Insulting {}'.format(target.mention))
            with urllib.request.urlopen('http://insult.mattbas.org/api/insult.txt?who=' + urllib.parse.quote_plus(target.name)) as f:
                insult = f.read().decode('utf-8')
                insult = insult.replace(target.name, target.mention)
                insults.append(insult)
        await client.send_message(message.channel, '\n'.join(insults))
    else:
        with urllib.request.urlopen('http://insult.mattbas.org/api/insult.txt') as f:
            insult = f.read().decode('utf-8')
            await client.send_message(message.channel, insult)

plugin = Plugin("Insult plugin", "Insults people")
plugin.addHandler(CommandHandler("!insult", insultHandler, "!insult [@User mention] - insult yourself without arguments or a user with a mention."))
