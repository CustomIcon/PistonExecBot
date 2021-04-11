from os import path
from configparser import ConfigParser
from pyrogram import Client
from piston import Piston
from .utils import langs

piston = Piston()



class bot(Client):
    def __init__(self, name):
        config_file = f"{name}.ini"
        config = ConfigParser()
        config.read(config_file)
        name = name.lower()
        plugins = {'root': path.join(__package__, 'plugins')}
        api_id = config.get('pyrogram', 'api_id')
        api_hash = config.get('pyrogram', 'api_hash')
        super().__init__(
            name,
            api_id=api_id,
            api_hash=api_hash,
            config_file=config_file,
            workers=16,
            plugins=plugins,
            workdir="./",
        )

    async def start(self):
        await super().start()
        await super().send_message(947138292, "Bot is online")
        languages = ''
        j = 1
        for v in (await piston.versions()):
            if j == 4:
                languages += f'|{(v.name+"-"+(v.version or "")):<15}|\n'
                j = 0
            else:
                languages += f'|{(v.name+"-"+(v.version or "")):<15}'
            j += 1
            langs.append(v)
        j += 1
        print('+===============================================================+')
        print('|                    Loaded Languages                           |')
        print('+=============+===============+================+===============+')
        print(languages)
        print('+===============+=============+===============+=================+')

        print("bot started. Hi.")

    async def stop(self, *args):
        await super().send_message(947138292, "Bot going offline")
        await super().stop()
        print("bot stopped. Bye.")
    