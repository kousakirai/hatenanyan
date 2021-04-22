import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class Virtualmoney(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  guild_ids = [774477394924666890]
  @cog_ext.cog_slash(name="money", guild_ids=guild_ids)
  async def _money(self, ctx: SlashContext):
    
    await ctx.send(content="所持金()：")
def setup(bot):
  return bot.add_cog(Virtualmoney(bot))