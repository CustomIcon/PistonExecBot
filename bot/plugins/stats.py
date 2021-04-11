from .execute import stdin as users
from .inline import execute as inline_users
from bot import bot, start_time
from bot.utils import time_parser
from pyrogram import filters
import time
import re


@bot.on_message(filters.command('stats'))
async def stats(_, message):
    uptime = time_parser((time.time() - start_time))
    await message.reply(
        f"**-Stats-**\n\n**Bot Uptime:** `{uptime}`\n**Successful Code Execution:** `{len(users)}`\n**Successful Inline Code Execution:** {len(inline_users)}"
    )

async def button_callback(_, __, query):
    if re.match(r'stats-', query.data):
        return True


button_create = filters.create(button_callback)



@bot.on_callback_query(button_create)
async def stats_button(client, query):
    message = query.data.split('-')
    start = float(message[1])
    end = float(message[2])
    await query.answer(
        f'Execute Time: {round((end - start) * 1000, 3)}ms',
        show_alert=True
    )
    
    