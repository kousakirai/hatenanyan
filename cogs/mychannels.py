import discord
from discord.ext import commands
from googlesearch import search
class my(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.group(name="mychannel", aliases="myc")
  async def mychannel(self, ctx):
    await ctx.send("準備中")