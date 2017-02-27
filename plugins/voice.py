import asyncio
import urllib.request
import discord.utils

from dev.plugin import *

# TODO: Make sending a clip easier

async def voiceHandler(client, message):
    # Grab the user who sent the message as a Member
    dest = discord.utils.get(message.server.members, name=message.author.name)

    # If the user isn't in a voice channel, we can't join anywhere
    if not dest.voice.voice_channel:
        await client.send_message(message.channel, 'You need to be a voice channel, bub.')
        return

    # We want to join the voice channel that the sender is in
    dest = dest.voice.voice_channel

    # If we are already connected voice, grab that voice object
    voice = client.voice_client_in(message.server)

    # If we aren't connected to voice, join the sender's channel
    # TODO: Handle moving channels if necessary
    if not voice or not voice.is_connected():
        voice = await client.join_voice_channel(dest)

    # Create and start the player
    player = voice.create_ffmpeg_player('rimshot.mp3')
    player.start()

    # Wait for the player to be done
    # TODO: better solution?
    while not player.is_done():
        await asyncio.sleep(0.5)

    # Disconnect from voice
    await voice.disconnect()

async def ytHandler(client, message):
    # Grab the user who sent the message as a Member
    dest = discord.utils.get(message.server.members, name=message.author.name)

    # If the user isn't in a voice channel, we can't join anywhere
    if not dest.voice.voice_channel:
        await client.send_message(message.channel, 'You need to be a voice channel, bub.')
        return

    # We want to join the voice channel that the sender is in
    dest = dest.voice.voice_channel

    # If we are already connected voice, grab that voice object
    voice = client.voice_client_in(message.server)

    # If we aren't connected to voice, join the sender's channel
    # TODO: Handle moving channels if necessary
    if not voice or not voice.is_connected():
        voice = await client.join_voice_channel(dest)

    # Create and start the player
    # player = await voice.create_ytdl_player('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    player = voice.create_ffmpeg_player('rr-short.mp4')
    player.start()

    # Wait for the player to be done
    # TODO: better solution?
    while not player.is_done():
        await asyncio.sleep(1)

    # Disconnect from voice
    await voice.disconnect()

plugin = Plugin("Voice fun", "Receive a friendly message from your Robot Overlord")
plugin.addHandler(CommandHandler("!badumts", voiceHandler, "!badumts - Tell your friend how funny he is"))
plugin.addHandler(CommandHandler("!rr", ytHandler, "!rr"))
