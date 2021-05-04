import discord
from discord.ext import commands


class role_add(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.ID_CHANNEL_README = 703465629000269855 # 該当のチャンネルのID
    self.ID_ROLE_WELCOME = 703451279489237042 # 付けたい役職のID 
    intents=discord.Intents.all()
    intents.reactions = True  
  @commands.Cog.listener
  async def on_raw_reaction_add(self, payload):

    channel = self.bot.get_channel(payload.channel_id)

    if channel.id != self.ID_CHANNEL_README:
        return

    guild = self.bot.get_guild(payload.guild_id)

    member = guild.get_member(payload.user_id)

    role = guild.get_role(self.ID_ROLE_WELCOME)

    await member.add_roles(role)

    await channel.send('いらっしゃいませ！')
def setup(bot):
  return bot.add_cog(role_add(bot))