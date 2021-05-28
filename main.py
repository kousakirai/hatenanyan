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
      embed1.add_field(name="あなたはすでに登録しています。",value='登録する必要はありません')
        
      await ctx.send(embed=embed1)
      return
      
    else:
        db.insert({'name':ctx.author.id, 'money':200})
        
        embed2 = discord.Embed(title="通貨システム",description=" ")
        embed2.add_field(name="ユーザー情報を登録しました。",value="登録記念に100ニャンコインを贈呈します")
        await ctx.send(Embed=embed2)

@slash.slash(name="money",guild_ids=guild_ids)
async def money(ctx):
  if not len(db.search(User.name==ctx.author.id)) > 0:
    await ctx.send(content="ユーザー情報が確認できませんでした。\n/setを実行してください。")
  else:
    a=db.search(User.name==ctx.author.id)
    l=int(a[0]["money"])/2
    await ctx.send(content=f'{l}ニャンコインです')


bot.author_id=757106917947605034

bot.load_extension("cogs.weakup")

bot.load_extension("jishaku")

keep_alive.keep_alive()

bot.run(os.getenv('TOKEN'))