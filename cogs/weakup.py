from discord.ext import commands
import discord
class weakup(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print('起動中です...')
    print(self.bot.user.name)
    print(self.bot.user.id)
    print('おはようございますマスター！()')
    await self.bot.change_presence(activity=discord.Game(name="こんにちはープレフィックスはh:だよー()", type=1))
    channel = self.bot.get_channel(818817278912626718)
    self.bot.load_extension("cogs.Block")

    self.bot.load_extension("adminonly.debug")

    self.bot.load_extension("cogs.users")

    self.bot.load_extension("cogs.music")

    self.bot.load_extension("cogs.NGwords")

    self.bot.load_extension("cogs.defult")

    self.bot.load_extension("cogs.News")

    self.bot.load_extension("cogs.wolf")

    self.bot.load_extension("cogs.reaction")

    self.bot.load_extension("cogs.slashcommand")
    
    self.bot.load_extension("cogs.log")
    await channel.send("```疑問猫Bot再起動しました。起動時になにかエラーが起きた場合は制作者のkousakiraiにお伝え下さい。社畜のように働きます()```")
    
def setup(bot):
  return bot.add_cog(weakup(bot))