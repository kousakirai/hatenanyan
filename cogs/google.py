import discord
from discord.ext import commands
from googlesearch import search
class google(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command()
  async def google(self, message):
    kensaku = message
    count = 0
    # 日本語で検索した上位5件を順番に表示
    for url in search(kensaku, lang="jp",num = 5):
        await message.send(url)
        count += 1
        if(count == 5):
            break
def setup(bot):
  return bot.add_cog(google(bot))