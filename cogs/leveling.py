import discord
from discord.ext import commands
from tinydb import TinyDB,Query
from tinydb.operations import increment

db = TinyDB('level.json')

User = Query()

class leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='addd')
    async def add(self, ctx):
        if len(db.search(User.name == ctx.author.id)) > 0:
            await ctx.send('追加済みです')

        else:
            db.insert({'name': ctx.author.id, 'age': 0})
            await ctx.send('追加しました')

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot:
            return

        channel = self.bot.get_channel(818817278912626718)

        if not message.channel == channel:
            return

        if "h:" in message.content:
            return

        if '' in message.content:
            db.update(increment('age'), User.name == message.author.id)
        a = db.search(User.name == message.author.id)
        if a:
            l = int(a[0]["money"]) / 2
            await self.bot.process_commands(message)
      

