import textwrap
import discord
import os
import keep_alive
import feedparser
from discord.ext import commands
from discord.ext.commands import CommandNotFound, CommandOnCooldown
from tinydb import TinyDB, Query
from Function.help import JapaneseHelpCommand
import async_google_trans_new
# 接続に必要なオブ
from discord_slash import SlashCommand

team_id = [
    739702692393517076, 693025129806037003, 757106917947605034,
    484655503675228171
]

class MyBot(commands.Bot):
    async def is_owner(self, user: discord.User):
        if user.id in team_id:
            return True
        return await super().is_owner(user)


prefix = "h?", "h:"
intents = discord.Intents.all()  # デフォルトのIntentsオブジェクトを生成
intents.typing = False

bot = MyBot(command_prefix=prefix,
            help_command=JapaneseHelpCommand(),
            intents=intents,
            case_insensitive=True)

slash = SlashCommand(bot, override_type=True, sync_commands=True)

db = TinyDB('money.json')

User = Query()

guild_ids = [774477394924666890]


bot.author_id = 757106917947605034

bot.load_extension("weakup")

bot.load_extension("jishaku")

bot.load_extension("discord_debug")

keep_alive.keep_alive()

bot.run(os.getenv('TOKEN'))
