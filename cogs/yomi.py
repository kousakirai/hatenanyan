import asyncio
from collections import deque
from tempfile import TemporaryFile
import asyncpg
import ast
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from gtts import gTTS
githublink = "https://github.com/TheUserCreated/python-discord-tts"
db_pass = ""
db_user = ""
table_name = "guilds"
config_options = ["whitelist", "blacklist", "blacklist_role", "whitelist_role"]
invite_link = "https://discord.com/api/oauth2/authorize?client_id=352643007918374912&permissions=36718656&scope=bot"

class yomiage(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  async def get_db_con():
      db = await asyncpg.connect(user=db_user, password=db_pass, database='postgres', host='127.0.0.1')

      return db


  async def update_config(self,guild, column, value):
    db = await self.get_db_con()
    await db.execute(f'UPDATE guilds SET {column} = $2 WHERE id = $1', guild.id, value)
    await db.close()


  @commands.Cog.listener()
  async def on_guild_join(self,guild):
      db = await self.get_db_con()
      await db.execute('''
                    INSERT INTO guilds(id, whitelist,blacklist,blacklist_role,whitelist_role) VALUES($1, $2, $3,$4,$5)
                ''', guild.id, False, False, 'none set', 'none set')

  @commands.group()
  async def yomi(self, ctx):
      if ctx.invoked_subcommand is None:
          await ctx.send('メインコマンドの後にサブコマンドが必要です。')
  @yomi.command()
  @has_permissions(administrator=True)
  async def blacklist(self, ctx, role):
      guild = ctx.message.guild
      if role == "false" or role == "False":
          await self.update_config(guild, "blacklist", "False")
      else:
          await self.update_config(guild, "blacklist", True)
          await self.update_config(guild, "blacklist_role", role)


  @yomi.command()
  @commands.is_owner()
  async def make_databases(self,ctx ):
      guild_list = self.bot.fetch_guilds()
      db = await self.get_db_con()
      await db.execute('''
            CREATE TABLE guilds(
                id bigint PRIMARY KEY,
                whitelist_role text,
                blacklist_role text,
                whitelist bool,
                blacklist bool
            )
          ''')
      async for guild in guild_list:
          await db.execute('''
                INSERT INTO guilds(id, whitelist,blacklist,blacklist_role,whitelist_role) VALUES($1, $2, $3,$4,$5)
            ''', guild.id, False, False, 'none set', 'none set')
      db.close()


  async def get_dbvalue(self,guild, value):
      db = await self.get_db_con()
      val = None
      for option in config_options:
          if value == option:
              val = await db.fetchval(f'SELECT {value} FROM guilds WHERE id = {guild.id}')
      await db.close()
      return val


  def insert_returns(self,body):
      # insert return stmt if the last expression is a expression statement
      if isinstance(body[-1], ast.Expr):
          body[-1] = ast.Return(body[-1].value)
          ast.fix_missing_locations(body[-1])

      # for if statements, we insert returns into the body and the or else
      if isinstance(body[-1], ast.If):
          self.nsert_returns(body[-1].body)
          self.insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
      if isinstance(body[-1], ast.With):
          self.insert_returns(body[-1].body)

  @yomi.command()
  async def join(self, ctx):
      try:
          channel = ctx.message.author.voice.channel
          await channel.connect()
          return
      except(TypeError, AttributeError):
          await ctx.send("ボイスチャンネルに接続してから再度実行してください。")
          return


  async def get_conf(self,guild, value):
      return await self.get_dbvalue(guild, value)


  @yomi.command()
  async def leave(self, ctx):
      try:
          await ctx.voice_client.disconnect(force=True)
          return
      except(TypeError, AttributeError):
          await ctx.send("ボイスチャンネルに接続されていません。")
          return


  @yomi.command()
  async def stop(self, ctx):  # just an alias for leave
      await self.leave(ctx)


  @yomi.command()
  async def say(self, ctx):
      message_queue = deque([])
      blacklist_status = await self.get_conf(ctx.message.guild, 'blacklist')
      can_speak = True
      if blacklist_status:
          blacklist_role = await self.get_conf(ctx.message.guild, 'blacklist_role')
          for role in ctx.message.author.roles:
              if role.name == blacklist_role:
                  can_speak = False
      if can_speak == False:
          return
      message = ctx.message.content[5:]
      usernick = ctx.message.author.display_name
      message = usernick + " says " + message
      try:
          vc = ctx.message.guild.voice_client
          if not vc.is_playing():
              tts = gTTS(message)
              f = TemporaryFile()
              tts.write_to_fp(f)
              f.seek(0)
              vc.play(discord.FFmpegPCMAudio(f, pipe=True))
          else:
              message_queue.append(message)
              while vc.is_playing():
                  await asyncio.sleep(0.1)
              tts = gTTS(message_queue.popleft())
              f = TemporaryFile()
              tts.write_to_fp(f)
              f.seek(0)
              vc.play(discord.FFmpegPCMAudio(f, pipe=True))
      except(TypeError, AttributeError):
          try:
              tts = gTTS(message)
              f = TemporaryFile()
              tts.write_to_fp(f)
              f.seek(0)
              channel = ctx.message.author.voice.channel
              vc = await channel.connect()
              vc.play(discord.FFmpegPCMAudio(f, pipe=True))
          except(AttributeError, TypeError):
              await ctx.send("I'm not in a voice channel and neither are you!")
              return
          f.close()
def setup(bot):
  return bot.add_cog(yomiage(bot))