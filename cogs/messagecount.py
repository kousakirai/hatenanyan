import discord
from discord.ext import commands
from tinydb import TinyDB,Query
from tinydb.operations import increment

db=TinyDB('db.json')

User=Query()

class count(commands.Cog):
    def __init__(self, bot):
        self.bot = bot    
        
    @commands.command(name='add')
    async def add(self,ctx):
      for entity in db.search(User.name==ctx.author.id):
          if entity['name'] == ctx.author.id:
              await ctx.send('追加済みです')
          
        
          else:
            db.insert({'name':ctx.author.id, 'age':0})

            await ctx.send('追加しました')
    
    @commands.Cog.listener()
    async def on_message(self, message):
      if message.author.bot:
        return
      
      if '' in message.content:        
        db.update(increment('age'),User.name==message.author.id)
        
        

    @commands.Cog.listener()
    async def on_member_join(self,member):
      if db.search(User.name==member.id) == member.id:
        db.insert({'name':member.id, 'age':0})

    @commands.command(name='dbtest')
    async def dbtest(self,ctx):
      a=db.search(User.name==ctx.author.id)
      await ctx.send(a)

def setup(bot):
    return bot.add_cog(count(bot))