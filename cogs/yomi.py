from discord.ext import commands
import discord
from ctypes import CDLL
class yomiage(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
      self.libc = CDLL("cogs/libAquesTalk10.so.1.1")
    
    @commands.group()
    async def yomi(self, ctx):
      if ctx.invoked_subcommand is None:
        await ctx.send('メインコマンドの後にサブコマンドが必要です。')
    
    @yomi.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.channel.send("あなたはボイスチャンネルに接続していません。")
            return
          # ボイスチャンネルに接続する
        self.on_vc = True
        await ctx.author.voice.channel.connect()
        await ctx.send("接続しました。")
    
    @yomi.command()
    async def leave(self, ctx):
      if ctx.guild.voice_client is None:
          await ctx.send("接続していません。")
          return
      if ctx.guild.voice_client.is_playing():
          await ctx.send("再生中です。")
          return 
      self.on_vc = False
      await ctx.guild.voice_client.disconnect()
      await ctx.send("切断しました。")
    
    @commands.Cog.listener()
    async def on_message(self, ctx):
      if self.on_vc == False:
        return
      koe = self.libc.AquesTalk_Synthe_Utf8(ctx)
      await ctx.guild.voice_client.play(koe)

def setup(bot): 
  return bot.add_cog(yomiage(bot))