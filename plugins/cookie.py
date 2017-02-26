import asyncio
import random

from dev.plugin import *
async def cookieHandler(client, message):
    hasTarget = len(message.content.split()) > 1
    if hasTarget:
        targets = message.mentions
        for target in message.mentions:
            if random.randint(1,100) > 75:
                await client.send_message(message.channel, "Cookie Monster ate {}'s cookie!".format(target.name))
            else:
                await client.send_message(message.channel, '{} got a cookie.'.format(target.name))
    else:
        if random.randint(1,100) > 75:
            await client.send_message(message.channel, 'Cookie Monster ate {} cookie!'.format(message.author.name))
        else:
            await client.send_message(message.channel, '{} got a cookie.'.format(message.author.name))

plugin = Plugin("Cookie plugin", "Might give a cookie")
plugin.addHandler(CommandHandler("!cookie", cookieHandler, "!cookie [@User mention] - might give a cookie to you or someone you mentioned."))