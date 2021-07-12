import discord
import json
from discord.ext import commands

with open("data.json", mode="r") as f:
    data = json.load(f)

levels = data["level"]


class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group()
    async def level(self, ctx):
      if ctx.invoked_subcommand is None:
        await ctx.send("サブコマンドが要ります")
        
    @level.command()
    async def check(self, ctx):
      if not str(ctx.author.id) in data["level"]:
        await ctx.send("まだカウントされていません")
      else:
        lev = data["level"][str(ctx.author.id)]["level"]
        embed = discord.Embed(title="レベリング機能",description=f"あなたのレベルは{lev}です。",color=0xff0000)
        embed.set_author(name=ctx.author,icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
        
    @level.command()
    @commands.has_permissions(administrator=True)
    async def block(self, ctx):
      data["level_block"].append(ctx.channel.id)
      with open("data.json", mode="w") as f:
        json.dump(data, f, indent=4)
      await ctx.send("レベル機能を無効にしました")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        data["level"][member.id] = {}
        data["level"][member.id]["level"] = 1
        data["level"][member.id]["exp"] = 0
        with open("data.json", mode="w") as f:
            json.dump(data, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.id in data["level_block"]:
            return
        if not str(message.author.id) in data["level"]:
          print("b")
          data["level"][message.author.id] = {}
          data["level"][message.author.id]["level"] = 1
          data["level"][message.author.id]["exp"] = 0
          with open("data.json", mode="w") as f:
            json.dump(data, f, indent=4)
        if str(message.author.id) in data["level"]:
          print("a")
          data["level"][str(message.author.id)]["exp"] += 1
          print(data["level"][str(message.author.id)]["exp"])
          with open("data.json", mode="w") as f:
            json.dump(data, f, indent=4)
          print("ok")
        ex = data["level"][str(message.author.id)]["exp"]
        lev = data["level"][str(message.author.id)]["level"]
        if int(ex) >= int(lev) * 2:
          print("c")
          data["level"][str(message.author.id)]["level"] += 1
          data["level"][str(message.author.id)]["exp"] = 0
          with open("data.json", mode="w") as f:
            json.dump(data, f, indent=4)
          lev2 = data["level"][str(message.author.id)]["level"]
          dm=await message.author.create_dm()
          await dm.send(f"あなたは{lev2}に上がりました")
          

def setup(bot):
     bot.add_cog(Level(bot))
