import discord
from discord.ext import commands

class wel(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.intents = discord.Intents.default()
    self.intents.members = True  
  @commands.Cog.listener(name="on_member_join")
  async def on_member_join(self, ctx, member: discord.Member):
    welcome_channel = 819716795433746453
    sys_channel = 821245836163547176
    await welcome_channel.send(f"{member}さん！いらっしゃいませ！\nまずはDMに送信されているメッセージをお読みください。")
    users = discord.Embed(title=f'{member}の詳細',
    description='詳細',color=discord.Color.orange())
    users.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    users.set_thumbnail(url=member.avatar_url)
    users.add_field(name='名前',value=f'**{member.display_name}#{member.discriminator}**')
    users.add_field(name='あなたはBot?', value=member.bot)
    users.add_field(name='作成時間', value=member.created_at, inline=False)
    users.add_field(name='サーバーに参加した時間', value=member.joined_at)
    await sys_channel.send(embed=users)
def setup(bot):
  return bot.add_cog(wel(bot))