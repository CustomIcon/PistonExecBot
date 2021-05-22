from bot import bot
from bot.utils import langs, lang_names
from pyrogram import types,  errors
from piston import Piston
import asyncio
import time

piston = Piston()

execute = {}

NEXT_OFFSET = 25

@bot.on_inline_query()
async def inline_exec(client, query):
    string = query.query
    offset = int(query.offset or 0)
    answers = []
    if string == '':
        for l in langs[offset: offset + NEXT_OFFSET]:
            answers.append(
                types.InlineQueryResultArticle(
                    title=l.language,
                    description=l.version or None,
                    input_message_content=types.InputTextMessageContent(
                        "**Language:** `{}`{}\nPress the button below to Execute your code:".format(
                            l.language,
                            '\n**Version:** `{}`'.format(l.version) or ''
                        )
                    ),
                    reply_markup=types.InlineKeyboardMarkup(
                        [
                            [
                                types.InlineKeyboardButton(
                                    'Execute',
                                    switch_inline_query_current_chat=l.language + " "
                                )
                            ]
                        ]
                    )
                )    
            )
    elif string.split()[0] in lang_names:
        if len(string.split()) == 1:
            await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text=f'Give a code to Excute in {string.split()[0]}',
                switch_pm_parameter='help_inline',
            )
            return
        source = string.split(None, 1)[1]
        start_time = time.time()
        for l in langs:
            if string.split()[0] == l.language:
                out = await piston.execute(
                    language=string.split()[0],
                    version=l.version,
                    source=source
                )
        try:

            msg = f"**Language:** `{out.language}-{out.version}`\n\n**Code:**\n```{source}```\n\n"
            if out.run:
                msg += f"**Output:**\n```{out.run.output}```\n\n"
            answers.append(
                types.InlineQueryResultArticle(
                    "Output:",
                    description=out.run.stdout or out.run.stderr,
                    input_message_content=types.InputTextMessageContent(
                        msg,
                        parse_mode='markdown'
                    ),
                    reply_markup=types.InlineKeyboardMarkup(
                        [
                            [
                                types.InlineKeyboardButton(
                                    'stats',
                                    callback_data=f'stats-{start_time}-{time.time()}'
                                )
                            ],
                            [
                                types.InlineKeyboardButton(
                                    'Fork',
                                    switch_inline_query_current_chat=f'{out.language} {source}'
                                ),
                                types.InlineKeyboardButton(
                                    'Try Again',
                                    switch_inline_query_current_chat=f'{out.language} '
                                ),    
                            ]
                            
                        ]
                    )
                )
            )
            execute[query.from_user.id] = True
        except AttributeError as err:
            answers.append(
                types.InlineQueryResultArticle(
                    "Error",
                    description=str(err),
                    input_message_content=types.InputTextMessageContent(
                        str(err),
                    )
                )
            )
        return await client.answer_inline_query(
                    query.id,
                    results=answers,
                    cache_time=0,
                )
    try:
        await client.answer_inline_query(
            query.id,
            results=answers,
            next_offset=str(offset + NEXT_OFFSET),
            cache_time=0,
        )
    except errors.exceptions.bad_request_400.QueryIdInvalid:
        return