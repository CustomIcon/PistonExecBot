from bot import bot
from pyrogram import filters
from bot.utils import langs, lang_names
from pyrogram import types
import time

from piston import Piston

piston = Piston()


stdin = {}
args = {}

@bot.on_message(
    filters.command("execute")
)
async def alive(client, message):
    try:
        stdin[message.from_user.id]
        args[message.from_user.id]
    except KeyError:
        stdin[message.from_user.id] = False
        args[message.from_user.id] = False
    buttons = []
    buton = types.InlineKeyboardMarkup(
        [
            [
                types.InlineKeyboardButton('✅ stdin' if stdin[message.from_user.id] else '❌ stdin', callback_data="stdin_trigger"),
                types.InlineKeyboardButton('✅ args' if args[message.from_user.id] else '❌ args', callback_data="args_trigger")
            ]
        ]
    )
    
    if len(message.text.split(None, 1)) == 2:
        lan = message.text.split(None, 1)[1]
        if lan not in lang_names:
            await message.reply("Wrong language of choice!")
            return
        else:
            codes = "**Language**: `{}`\n\nGive me a code to execute:".format(lan)
    else:
        for l in langs:
            buttons.append([types.KeyboardButton(l.name + " " + (l.version or ""))])
        language = await client.ask(
            message.chat.id,
            f"pick a language from Keyboard:",
            reply_markup=types.ReplyKeyboardMarkup(buttons),
            reply_to_message_id=message.message_id
        )
        lan = language.text.split(None, 1)
        if lan[0] not in lang_names:
            await message.reply("Wrong language of choice", reply_markup=types.ReplyKeyboardRemove())
            return   
        try:
            codes = "**Language**: `{}`\n**Version**: `{}`\n\nGive me a code to execute:".format(lan[0], lan[1])
        except IndexError:
            codes = "**Language**: `{}`\n\nGive me a code to execute:".format(lan[0])
    await message.reply("got it!", reply_markup=types.ReplyKeyboardRemove())
    source = await client.ask(
        message.chat.id,
        text=codes,
        reply_to_message_id=message.message_id,
        reply_markup=buton
    )
    if stdin[message.from_user.id]:
        std = await client.ask(
            message.chat.id,
            text="give me your input to the code",
            reply_to_message_id=message.message_id,
        )
        std = std.text
    else:
        std = None
    if args[message.from_user.id]:
        arg = await client.ask(
            message.chat.id,
            text="give me arguments to the code separated by a 'space'",
            reply_to_message_id=message.message_id,
        )
        arg = arg.text.split(" ")
    else:
        arg = None
    start_time = time.time()
    output = await piston.execute(
        language=lan if len(message.text.split(None, 1)) == 2 else lan[0],
        source=source.text,
        stdin=std,
        args=arg
    )
    out = "**-Result-**\n"
    try:
        if output.language:
            out += f"**Language**: ```{output.language}```\n\n"
        # if output.output:
        #     out += f"**Output**:\n```{output.output}```\n\n"
        if output.stdout:
            out += f"**Stdout**:\n```{output.stdout}```\n\n"
        if output.stderr:
            out += f"**Stderr**:\n```{output.stderr}```"        
        await message.reply(
            out,
            reply_markup=types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton(
                            'stats',
                            callback_data=f'stats-{start_time}-{time.time()}'
                        )
                    ]
                ]
            )
        )
        
    except AttributeError:
        await message.reply("Code Execution was not Successful!")
        


@bot.on_callback_query(filters.regex("^stdin_trigger"))
async def stdin_triggerer(client, query):
    if stdin[query.from_user.id]:
        stdin[query.from_user.id] = False
        await query.message.edit_reply_markup(
            types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton(
                            '✅ stdin' if stdin[query.from_user.id] else '❌ stdin',
                            callback_data="stdin_trigger"
                        ),
                        types.InlineKeyboardButton(
                            '✅ args' if args[query.from_user.id] else '❌ args',
                            callback_data="args_trigger"
                        )
                    ]
                ]
            )
        )
        await query.answer("stdin was Disabled")
    else:
        stdin[query.from_user.id] = True
        await query.message.edit_reply_markup(
            types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton(
                            '✅ stdin' if stdin[query.from_user.id] else '❌ stdin',
                            callback_data="stdin_trigger"
                        ),
                        types.InlineKeyboardButton(
                            '✅ args' if args[query.from_user.id] else '❌ args',
                            callback_data="args_trigger"
                        )
                    ]
                ]
            )
        )
        await query.answer("stdin was Enabled")
        

@bot.on_callback_query(filters.regex("^args_trigger"))
async def args_triggerer(client, query):
    if args[query.from_user.id]:
        args[query.from_user.id] = False
        await query.message.edit_reply_markup(
            types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton(
                            '✅ stdin' if stdin[query.from_user.id] else '❌ stdin',
                            callback_data="stdin_trigger"
                        ),
                        types.InlineKeyboardButton(
                            '✅ args' if args[query.from_user.id] else '❌ args',
                            callback_data="args_trigger"
                        )
                    ]
                ]
            )
        )
        await query.answer("args was Disabled")
    else:
        args[query.from_user.id] = True
        await query.message.edit_reply_markup(
            types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton(
                            '✅ stdin' if stdin[query.from_user.id] else '❌ stdin',
                            callback_data="stdin_trigger"
                        ),
                        types.InlineKeyboardButton(
                            '✅ args' if args[query.from_user.id] else '❌ args',
                            callback_data="args_trigger"
                        )
                    ]
                ]
            )
        )
        await query.answer("args was Enabled")