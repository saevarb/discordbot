import asyncio
import urllib.request
import discord.utils

from dev.plugin import *

# TODO: Make sending a clip easier

async def rimshotHandler(client, message):
    # Grab the user who sent the message as a Member
    dest = discord.utils.get(message.server.members, name=message.author.name)

    # If the user isn't in a voice channel, we can't join anywhere
    if not dest.voice.voice_channel:
        await client.send_message(message.channel, 'You need to be a voice channel, bub.')
        return

    # We want to join the voice channel that the sender is in
    dest = dest.voice.voice_channel
    client.voiceCount += 1
    await client.voiceQueue.put((client.voiceCount, SoundCommand('rimshot.mp3', dest, disconnectAfter=False)))


async def rrHandler(client, message):
    # Grab the user who sent the message as a Member
    dest = discord.utils.get(message.server.members, name=message.author.name)

    # If the user isn't in a voice channel, we can't join anywhere
    if not dest.voice.voice_channel:
        await client.send_message(message.channel, 'You need to be a voice channel, bub.')
        return

    # We want to join the voice channel that the sender is in
    dest = dest.voice.voice_channel
    client.voiceCount += 1
    await client.voiceQueue.put((client.voiceCount, SoundCommand('rr-short.mp4', dest)))


async def stopHandler(client, message):
    await client.voiceQueue.put((0, StopCommand()))

plugin = Plugin("Voice fun", "Receive a friendly message from your Robot Overlord")
plugin.addHandler(CommandHandler("!badumts", rimshotHandler, "!badumts - Tell your friend how funny he is"))
plugin.addHandler(CommandHandler("!rr", rrHandler, "!rr - Profess your love for your comrades"))
plugin.addHandler(CommandHandler("!stop", stopHandler, "!stop - Stop the currently playing sound"))
