import urllib.request as r
import urllib.parse as up
import json
import random
import discord
from dev.plugin import *
from imgurpython import ImgurClient
import re

client_id = 'afcf62c93f3ea46	'
client_secret = '38352d63a985b8a780fbcb6da95e01eab969d554'

imgur = ImgurClient(client_id, client_secret)

# Example request
def asCode(s):
    return "```\n" + s + "\n```\n"

def loadMemes(client):
    if not hasattr(client, 'memes') :
        req = r.Request('https://api.imgflip.com/get_memes', headers={'User-Agent': 'Chrome'})
        with r.urlopen(req) as response:
            res = response.read()
            client.memes = json.loads(res)['data']['memes']
            print('Loaded memes')

async def fooHandler(client, msg):
    await client.delete_message(msg)
    loadMemes(client)
    memeList = []
    for meme in client.memes:
        memeList.append(f"{meme['name']} - {meme['id']}\n")
    numMemes = len(memeList)
    offset = int(numMemes / 2)
    await client.send_message(msg.author, asCode("\n".join(memeList[:offset])))
    await client.send_message(msg.author, asCode("\n".join(memeList[offset:])))


async def genHandler(client, msg):
    splits = msg.content.split()
    await client.delete_message(msg)

    if len(splits) < 4:
        return

    top = []
    stop = 0
    for i, s in enumerate(splits[2:]):
        top.append(s.replace('"', ''))
        if s.endswith('"'):
            stop = i
            break
    bottom = []

    for i, s in enumerate(splits[stop + 3:]):
        bottom.append(s.replace('"', ''))
        if s.endswith('"'):
            break

    postData = up.urlencode([('username', 'sbrg'),
                             ('password', 'foobar123'),
                             ('template_id', splits[1]),
                             ('text0', " ".join(top)),
                             ('text1', " ".join(bottom))
    ])

    print(postData)

    req = r.Request('https://api.imgflip.com/caption_image',
                    method='POST', headers={'User-Agent': 'Chrome'},
                    data=postData.encode())
    with r.urlopen(req) as response:
        res = json.loads(response.read())
        em = discord.Embed(description=" ".join(bottom), title=" ".join(top))
        parsed = up.urlparse(res['data']['url'])._replace(scheme='https')
        em.set_image(url=parsed.geturl()).set_thumbnail(url=parsed.geturl())
        await client.send_message(msg.channel, embed=em)


async def searchHandler(client, msg):
    loadMemes(client)
    splits = msg.content.split()
    if len(splits) < 2:
        return

    regex = " ".join(splits[1:])
    matches = []
    for meme in client.memes:
        if re.match(f".*{regex}.*", meme['name'], flags=re.I):
            matches.append(f"{meme['name']} - {meme['id']}\n")
    if matches:
        await client.send_message(msg.channel, "\n".join(matches))
    else:
        await client.send_message(msg.channel, "No matches, sorry.")



plugin = Plugin("Meme plugin", "Generate memes")
plugin.addHandler(CommandHandler("!memes.list", fooHandler, "!memes.list - List available memes and their IDs for the generator"))
plugin.addHandler(CommandHandler("!memes.gen", genHandler, '!memes.gen [Meme ID] "Top text in quotes" "Bottom text in quotes"'))
plugin.addHandler(CommandHandler("!memes.find", searchHandler, '!memes.find [Pattern] - Search for meme using part of name'))
