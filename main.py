import discord
import os
import keep_alive
import feedparser
from discord.ext import commands
from discord.ext.commands import CommandNotFound, CommandOnCooldown
from cogs.help import JapaneseHelpCommand
# 接続に必要なオブジェクトを生成
from discord_slash import SlashCommand
prefix = "h?", "h:"

bot = commands.Bot(command_prefix=prefix,help_command=JapaneseHelpCommand(), 
case_insensitive=True,
intents=discord.Intents.all())
slash = SlashCommand(bot, override_type = True, sync_commands=True)

bot.author_id=757106917947605034

bot.load_extension("cogs.weakup")

bot.load_extension("jishaku")

keep_alive.keep_alive()

bot.run(os.getenv('TOKEN'))