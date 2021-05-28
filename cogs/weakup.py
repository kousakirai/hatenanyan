from discord.ext import commands
import discord
import asyncio
from discord.ext.commands import CommandNotFound, CommandOnCooldown
class weakup(commands.Cog):
  def __init__(self, bot):
    self.bot = bot


  async def status_task(self):
    while True:
        guild = self.bot.get_guild(774477394924666890)
        user_count = sum(1 for member in guild.members if not member.bot)
        game = discord.Game(f"In {user_count} users.")
        await self.bot.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(30)
  
  
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    ch = 832560631818485790
    embed = discord.Embed(title="エラー情報", description="", color=0xf00)
    embed.add_field(name="エラー発生サーバー名", value=ctx.guild.name, inline=False)
    embed.add_field(name="エラー発生サーバーID", value=ctx.guild.id, inline=False)
    embed.add_field(name="エラー発生ユーザー名", value=ctx.author.name, inline=False)
    embed.add_field(name="エラー発生ユーザーID", value=ctx.author.id, inline=False)
    embed.add_field(name="エラー発生コマンド", value=ctx.message.content, inline=False)
    embed.add_field(name="発生エラー", value=error, inline=False)
    m = await self.bot.get_channel(ch).send(embed=embed)
    await ctx.send(f"何らかのエラーが発生しました。ごめんなさい。\nこのエラーについて問い合わせるときはこのコードも一緒にお知らせください：{m.id}")
  
  
  
  
  @commands.Cog.listener()
  async def on_ready(self):
    print('起動中です...')
    print(self.bot.user.name)
    print(self.bot.user.id)
    print('おはようございますマスター！()')
    channel = self.bot.get_channel(818817278912626718)
    self.bot.load_extension("cogs.Block")
    
    self.bot.load_extension("adminonly.debug")

    self.bot.load_extension("cogs.users")

    self.bot.load_extension("cogs.music")

    self.bot.load_extension("cogs.NGwords")

    self.bot.load_extension("cogs.defult")

    self.bot.load_extension("cogs.News")
    
    self.bot.load_extension("cogs.messagecount")
   
    self.bot.load_extension("cogs.reaction")
    
    self.bot.load_extension("cogs.welcome")
    
    self.bot.load_extension("cogs.log")
    
    await channel.send("```疑問猫Bot再起動しました。起動時になにかエラーが起きた場合は制作者のkousakiraiにお伝え下さい。社畜のように働きます()```")
     
    self.bot.loop.create_task(self.status_task())

def setup(bot):
  return bot.add_cog(weakup(bot))