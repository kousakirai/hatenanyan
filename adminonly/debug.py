import sys
import os                               
import discord
from discord.ext import commands
class debug(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.group(name="debug")
  async def debug(self, ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('メインコマンドの後にサブコマンドが必要です()')
  @debug.command(name="reload2",aliases=["r2"])
  @commands.has_permissions(manage_roles=True)
  async def reload2(self, ctx, name):  
    role = ctx.guild.get_role(813389100815351869)
    if ctx.author.guild_permissions.administrator or role in ctx.author.roles:
      try:
          self.bot.reload_extension(f"adminonly.{name}")
      except Exception as e:
          await ctx.send('**エラー**' + '\n'.join(e.args))
      else:
          await ctx.send(f"cogs.{name}のリロードに成功しました()")
    else:
        await ctx.send("あなたには権限がありません()")
  @debug.command(name="reload",aliases=["re"])
  @commands.has_permissions(manage_roles=True)
  async def reload1(self, ctx, name):
    role = ctx.guild.get_role(813389100815351869)
    if ctx.author.guild_permissions.administrator or role in ctx.author.roles:
      try:
          self.bot.reload_extension(f"cogs.{name}")
      except Exception as e:
          await ctx.send('**エラー**' + '\n'.join(e.args))
      else:
          await ctx.send(f"cogs.{name}のリロードに成功しました()")
    else:
        await ctx.send("あなたには権限がありません()")
  @debug.command(name="reboot")
  async def reboot(self, ctx):
    role = ctx.guild.get_role(813389100815351869)
    if ctx.author.guild_permissions.administrator or role in ctx.author.roles:
      await ctx.send("Botを再起動します。")
      await self.bot.change_presence(activity=discord.Game(name="reboot...", type=1))      
      python = sys.executable 
      os.execl(python, python, *sys.argv)
    else:
        await ctx.send("あなたには権限がありません()")
  @debug.command()
  async def eval(self, message):
    role = message.guild.get_role(813389100815351869)
    if message.author.guild_permissions.administrator or role in message.author.roles:
      if message.content.startswith("/eval await "):
          src = message.content.split(" ", 2)[-1].lstrip()
          await eval(src)
      elif message.content.startswith("/eval"):
        src = message.content.split(" ", 2)[-1].lstrip()
        await eval(src)
def setup(bot):
  return bot.add_cog(debug(bot))