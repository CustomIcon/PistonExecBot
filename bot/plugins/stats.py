from .start import stdin as users
from bot import bot, start_time
from bot.utils import time_parser
from pyrogram import filters
import time


@bot.on_message(filters.command('stats'))
async def stats(_, message):
    uptime = time_parser((time.time() - start_time))
    await message.reply(
        f"**-Stats-**\n\n**Bot Uptime:** `{uptime}`\n**Successful Code Execution:** `{len(users)}`"
    )