import discord
from discord.ext import commands
import os
import aiofile
import json
class wolf(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.path = os.path.dirname(__file__) + "/txtfiles/wolfplayer.json"
    with open(self.path, "r") as f:
        content = f.read()
    self.content = json.loads(content)
  async def create_channel(self, message, channel_name):
    category = message.guild.get_channel(834672775011762176)
    new_channel = await category.create_text_channel(name=channel_name)
    return new_channel
  @commands.group()
  async def wolf(self, ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('メインコマンドの後にサブコマンドが必要です。')
  @wolf.command()
  async def create(self,ctx):
    # チャンネルを作成する非同期関数を実行して Channel オブジェクトを取得
    new_channel = await self.create_channel(ctx, channel_name="人狼ルーム")
    # チャンネルのリンクと作成メッセージを送信
    text = f'{new_channel.mention} を作成しました'
    await ctx.send(text)
  @wolf.command()
  async def join(self, message):
    id = str(message.author.id)
    idlist = str(self.content)
    for word in idlist:
        if word in id:
            await message.send("あなたはすでに参加しています。")
            return
    self.content.append(id)
    async with aiofile.async_open(self.path, "w", encoding = "utf_8") as f:
        await f.write(json.dumps(self.content))
    await message.send(f"{message.author.mention}さんがゲームに参加しました。")
  
  @wolf.command()
  async def leave(self, message):
    id = str(message.author.id)
    idlist = str(self.content)
    for word in idlist:
      if not word in id:
          return await message.send("あなたはゲームに参加していません。")    
      self.content.remove(id)
      async with aiofile.async_open(self.path, "w", encoding = "utf_8") as f:
          await f.write(json.dumps(self.content))
      await message.send("参加を取り消しました。")

def setup(bot):
  return bot.add_cog(wolf(bot))