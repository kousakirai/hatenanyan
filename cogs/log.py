import discord
from discord.ext import commands
from datetime import datetime
import pytz

class log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_message(self, message):
      if message.author.bot:
        return 
      now = datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%D:%H:%M')
      embed=discord.Embed(title="メッセージログ",description=f"メッセージを取得しました。\n時刻"+now ,color=0x00ff00)
      embed.add_field(name="発言者",value=f"{message.author.mention}({message.author})\nID:{message.author.id}",inline=False)
      embed.add_field(name="チャンネル",value=f"{message.channel.mention}({message.channel.name})\nID:{message.channel.id}",inline=False)
      embed.add_field(name="メッセージ内容",value="なし" if not message.content else message.content,inline=False)
      channel = self.bot.get_channel(8(818817278912626718)
      await channel.send(embed=embed)
def setup(bot):
  return bot.add_cog(log(bot))
