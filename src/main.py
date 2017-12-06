#!/usr/bin/env python3.6
import asyncio
import logging
import discord
import discord.opus
import discord.ext.commands
from dev.plugin import *
from typing import *
import random

client = discord.Client()
client.plugins = loadPlugins()
# TODO: Necessary?
# discord.opus.load_opus()

client.voiceQueue = asyncio.Queue()
client.voiceCount = 0
client.player = None

async def voiceWorker():
    await client.wait_until_ready()

    while not client.is_closed:
        (pri, voiceCmd) = await client.voiceQueue.get()
        print("received message: " + str((pri, voiceCmd)))

        if isinstance(voiceCmd, StopCommand):
            if client.player and client.player.is_playing():
                client.player.stop()
                continue
        else:
            if client.player and client.player.is_playing():
                await client.voiceQueue.put((pri, voiceCmd))
                await asyncio.sleep(2)
                # Disconnect from voice
                if client.player.is_done() and voiceCmd.disconnectAfter:
                    await voice.disconnect()
                continue

            # If we are already connected voice, grab that voice object
            # voice is None if we are not connected to voice on this server
            voice = client.voice_client_in(voiceCmd.dest.server)

            if not voice:
                # If we aren't connecteded to voice at all, join voice and channel
                voice = await client.join_voice_channel(voiceCmd.dest)
            elif voice.is_connected():
                # If we are connected, move to the channel
                voice.move_to(voiceCmd.dest)

            if isinstance(voiceCmd, VoiceCommand):
                client.player = voice.create_ffmpeg_player(voiceCmd.url)
            elif isinstance(voiceCmd, YoutubeCommand):
                client.player = voice.create_ytdl_player(voiceCmd.url)

            client.player.start()



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message : discord.Message):
    print("{} said: {}".format(message.author.name, message.content))
    for plugin in client.plugins.values():
        await plugin.runPlugin(client, message)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

with open('.token.secret') as f:
    token = f.readline()
    client.loop.create_task(voiceWorker())
    client.run(token)
