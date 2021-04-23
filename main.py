import discord
import os
import keep_alive
from discord.ext import commands
from discord.ext.commands import CommandNotFound, CommandOnCooldown
from cogs.help import JapaneseHelpCommand
# 接続に必要なオブジェクトを生成
from discord_slash import SlashCommand
prefix = "h?", "h:"

bot = commands.Bot(command_prefix=prefix,help_command=JapaneseHelpCommand(), intents=discord.Intents.all())
slash = SlashCommand(bot, override_type = True, sync_commands=True)


bot.load_extension("cogs.weakup")
keep_alive.keep_alive()

bot.run(os.getenv('TOKEN'))