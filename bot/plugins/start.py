from bot import bot
from pyrogram import filters, types


@bot.on_message(filters.command('start'))
async def start_handle(client, message):
    if len(message.text.split()) >= 2:
        if message.text.split()[1] == 'help_inline':
            await message.reply(
                "**How to use @pistonexecbot via inline\n\n type in `@pistonexecbot` <language> <code>**\n\n See /langs for loaded languages",
                reply_markup=types.InlineKeyboardMarkup(
                    [
                        [
                            types.InlineKeyboardButton(
                                'Example',
                                switch_inline_query_current_chat='python3 print("Hello World")'
                            )
                        ]
                    ]
                )
            )
    else:
        await message.reply(
            "**Usage**\n"
            "`/execute` or `/execute [language]` if you want to go for a quick code execution.\n\n"
            "Executing files are not supported yet but will in future\n\n"
            "you can also use me via inline:\n`@pistonexecbot python3 print('Hello World')`\n\n"
            "all available languages can be seen on /langs"
        )