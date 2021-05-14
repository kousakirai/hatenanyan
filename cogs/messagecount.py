import discord
from discord.ext import commands
from tinydb import TinyDB,Query
from tinydb.operations import increment
User=Query()

db=TinyDB('db.json')

class count(commands.Cog):
    def __init__(self, bot):
        self.bot = bot    
    
    @commands.command(name='add')
    async def add(self,ctx):
      if db.search(User.name==ctx.author.id) == ctx.author.id:
        await ctx.send("あなたはすでに登録されています。")
        return
      else:
        db.insert({'name':ctx.author.id, 'age':0})
        
    @commands.Cog.listener()
    async def on_message(self, message):
      if message.content == 'test':
        db.update(increment('age'),User.name==message.author.id)

    @commands.command(name='dbtest')
    async def dbtest(self,ctx):
      a=db.search(User.name==ctx.author.id)
      await ctx.send(a)

def setup(bot):
    return bot.add_cog(count(bot))