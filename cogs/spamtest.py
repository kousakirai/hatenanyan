import discord
from discord.ext import commands
from datetime import datetime
import pytz
class anti_spam(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, message):
    old_message = []
    if message.content == old_message:
      now = datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%D:%H:%M')
      await message.channel.send(f"{message.author.mention},NGワードを発言したためメッセージを削除しました。")
      embed=discord.Embed(title="NGワード削除ログ",description=f"NGワードの削除が行われました。\n時刻"+now,color=0xff0000)
      embed.add_field(name="対象者",value=f"{message.author.mention}({message.author})\nID:{message.author.id}",inline=False)
      embed.add_field(name="チャンネル",value=f"{message.channel.mention}({message.channel.name})\nID:{message.channel.id}",inline=False)
      embed.add_field(name="メッセージ内容",value=message.content.replace(word,f"||{word}||"),inline=False)
      await message.delete()
    else:
        return
    