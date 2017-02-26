import discord
import asyncio
import http.client
import urllib.request
import logging
import json
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        # await client.delete_message(message)
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    if message.content.startswith('!insult'):
        hasTarget = len(message.content.split()) > 1

        if hasTarget:
            targets = message.mentions
            for target in message.mentions:
                print('Insulting {}'.format(target.mention))
                with urllib.request.urlopen('http://insult.mattbas.org/api/insult.txt?who=' + target.name) as f:
                    insult = f.read().decode('utf-8')
                    insult = insult.replace(target.name, target.mention)
                    await client.send_message(message.channel, insult)
        else:
            with urllib.request.urlopen('http://insult.mattbas.org/api/insult.txt') as f:
                insult = f.read().decode('utf-8')
                await client.send_message(message.channel, insult)

    if message.content.startswith('!chuck'):
        with urllib.request.urlopen('http://api.icndb.com/jokes/random') as f:
            chuck = f.read().decode('utf-8')
            asJson = json.loads(chuck)
            await client.send_message(message.channel, asJson['value']['joke'])

    if message.content.startswith('!yoMomma'):
        with urllib.request.urlopen('http://api.yomomma.info/') as f:
            momma = f.read().decode('utf-8')
            asJson = json.loads(momma)
            await client.send_message(message.channel, asJson['joke'])


    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

with open('.token.secret') as f:
    token = f.readline()
    client.run(token)
