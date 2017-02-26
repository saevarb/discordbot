import asyncio
import urllib.request
 
from dev.plugin import *

async def reloadHandler(client, message):
    tmp = await client.send_message(message.channel, "Reloading plugins..")
    client.plugins = loadPlugins()
    await client.edit_message(tmp, "Plugins reloaded!")

async def listHandler(client, message):
    for (k, p) in client.plugins.items():
        formatted = "{} - {} - {}".format(k, p.name, p.help)
        await client.send_message(message.channel, formatted)
    await client.send_message(message.channel, "For more information, type `!help [plugin.thing]`")


plugin = Plugin("Plugin plugin", "Commands for reloading plugins and listing commands")
plugin.addHandler(CommandHandler("!reload", reloadHandler, "Reloads all plugins"))
plugin.addHandler(CommandHandler("!help", listHandler, "List plugins"))
