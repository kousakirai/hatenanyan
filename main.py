import discord
import os
import keep_alive
import feedparser
from discord.ext import commands
from discord.ext.commands import CommandNotFound, CommandOnCooldown
from tinydb import TinyDB,Query
from cogs.help import JapaneseHelpCommand
# 接続に必要なオブジェクトを生成
from discord_slash import SlashCommand
prefix = "h?", "h:"

bot = commands.Bot(command_prefix=prefix,help_command=JapaneseHelpCommand(), intents=discord.Intents.all(), case_insensitive=True)
slash = SlashCommand(bot, override_type = True, sync_commands=True)

db=TinyDB('money.json')

User=Query()

guild_ids=[774477394924666890]

@slash.slash(name="set",guild_ids=guild_ids)
async def add(ctx):
    if len(db.search(User.name==ctx.author.id)) > 0:
        
      embed1 = discord.Embed(title="通貨システム", description=' ')
      embed1.add_field(name="あなたはすでに登録しています。",value=' ')
        
      await ctx.send(content='あなたは既に登録してあります')
      return
      
    else:
        db.insert({'name':ctx.author.id, 'money':0})
        
        embed2 = discord.Embed(title="通貨システム",description=" ")
        embed2.add_field(name="ユーザー情報を登録しました。",value=" ")
        await ctx.send(content='追加しました')

@slash.slash(name="money",guild_ids=guild_ids)
async def money(ctx):
  if not len(db.search(User.name==ctx.author.id)) > 0:
    await ctx.send(content="ユーザー情報が確認できませんでした。\n/setを実行してください。")
  else:
    zangaku = db.search(User.name==ctx.author.id)
    await ctx.send(content=f'{zangaku[0]["money"]}円です')

bot.author_id=757106917947605034

bot.load_extension("cogs.weakup")

bot.load_extension("jishaku")

keep_alive.keep_alive()

bot.run(os.getenv('TOKEN'))