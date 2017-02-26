import urllib.request
import json
import random
from dev.plugin import *
from imgurpython import ImgurClient

client_id = 'afcf62c93f3ea46	'
client_secret = '38352d63a985b8a780fbcb6da95e01eab969d554'

imgur = ImgurClient(client_id, client_secret)

# Example request
async def fooHandler(client, msg):
    req = urllib.request.Request('http://api.imgflip.com/get_memes')
    req.add_header('User-Agent', 'GoogleBot')
    with urllib.request.urlopen(req) as f:
        # items = imgur.memes_subgallery(sort='viral', page=0, window='week')
        items = imgur.gallery(section='hot', sort='viral', page=0, window='day', show_viral=True)
        i = random.randint(0, len(items))
        chosen = items[i]
        if chosen.is_album:
            imgs = imgur.get_album_images(items[i].id)
            await client.send_message(msg.channel, imgs[0].link)
        else:
            await client.send_message(msg.channel, chosen.link)


plugin = Plugin("Meme plugin", "This is a very dank meme plugin for all your meme needs")
plugin.addHandler(CommandHandler("!dank", fooHandler, "!dank - Increase dankness of channel"))
