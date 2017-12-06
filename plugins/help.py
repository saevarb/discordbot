import asyncio
import urllib.request
 
from dev.plugin import *


async def reloadHandler(client, message):
    await client.delete_message(message)
    tmp = await client.send_message(message.channel, "Reloading plugins..")
    client.plugins = loadPlugins()
    await client.edit_message(tmp, "Plugins reloaded!")

async def helpHandler(client, message):
    splits = message.content.split()
    output = []
    if len(splits) > 1:
        plug = client.plugins[splits[1]]
        output.append("Information for __**{}**__".format(splits[1]))
        for h in plug.handlers:
            output.append(h.help)
    else:
        for (k, p) in client.plugins.items():
            formatted = "__**{}**__ - {} - {}".format(k, p.name, p.help)
            output.append(formatted)
        output.append( "\nFor more information, type `!help [plugins.thing]`")
    await client.send_message(message.channel, '\n'.join(output))


plugin = Plugin("Help plugin", "Information about plugins")
plugin.addHandler(CommandHandler("!reload", reloadHandler, "!reload - Reloads all plugins"))
plugin.addHandler(CommandHandler("!help", helpHandler, "!help - Show help information"))
