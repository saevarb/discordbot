import importlib.util
import glob
import os

def loadPlugins():
    modules = {}
    for path in glob.glob('plugins/*.py'):

        plugName = os.path.splitext(path.replace(os.sep, '.'))[0]

        spec = importlib.util.spec_from_file_location(plugName, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        modules[plugName] = module.plugin
    return modules

class VoiceCommand(object):
    def __init__(self, url, dest, disconnectAfter=True):
        self.url = url
        self.dest = dest
        self.disconnectAfter = disconnectAfter

class YoutubeCommand(VoiceCommand):
    def __init__(self, url, dest, disconnectAfter=True):
        super().__init__(url, dest, disconnectAfter)

class SoundCommand(VoiceCommand):
    def __init__(self, url, dest, disconnectAfter=True):
        super().__init__(url, dest, disconnectAfter)

class StopCommand(VoiceCommand):
    def __init__(self):
        super().__init__(None, None)

class Plugin():
    def __init__(self, name, help):
        self.name = name
        self.handlers = []
        self.help = help

    def __repr__(self):
        return "Plugin('{}', '{}')".format(self.name, self.help)

    def __str__(self):
        self.__repr__()

    def addHandler(self, handler):
        self.handlers.append(handler)

    async def runPlugin(self, client, message):
        for handler in self.handlers:
            await handler.run(client, message)

class CustomHandler():
    def __init__(self, predicate, function, help):
        self.predicate = predicate
        self.function = function
        self.help = help

    async def run(self, client, message):
        if self.predicate(message):
            await self.function(client, message)

class CommandHandler(CustomHandler):
    def __init__(self, command, function, help):
        super().__init__(lambda m: m.content.startswith(command), function, help)
