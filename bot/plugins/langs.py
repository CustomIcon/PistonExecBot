from bot import bot
from bot.utils import langs
from pyrogram import filters
from piston import Piston

piston = Piston()


@bot.on_message(filters.command('langs'))
async def languages(client, message):
    j = 0
    languages = ''
    for v in (await piston.versions()):
        if j == 2:
            languages += f'|{(v.language+""):<16}|{(v.version or ""):<16}|\n'
            j = 0
        else:
            languages += f'|{(v.language+""):<16}|{(v.version or ""):<16}|\n'
        j += 1
        langs.append(v)
    j += 1
    await message.reply(
        '```+=================================+\n'
        '|        Loaded Languages         |\n'
        '+=================================+\n'
        '|    Languages   |    Version     |'
        f'\n+=================================+\n{languages}'
        '+=================================+```'
    )