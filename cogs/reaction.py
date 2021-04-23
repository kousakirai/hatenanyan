import discord
from discord.ext import commands


class role_add(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.ID_CHANNEL_README = 828936225897054218 # 該当のチャンネルのID
    self.ID_ROLE_WELCOME = 828937443972612117 # 付けたい役職のID
    intents=discord.Intents.all()
    intents.reactions = True  
  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
      if payload.member.bot: # BOTアカウントは無視する
          return

      if payload.channel_id != 123456789123: # 特定のチャンネル以外でリアクションした場合は無視する
          return

      if payload.emoji.name == "👍": # 特定の絵文字
          await payload.member.add_roles(
              payload.member.guild.get_role(123456789123) # ロールID
            )

  @commands.Cog.listener()
  async def on_raw_reaction_remove(self, payload):
    guild = self.bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if guild is None or member is None: # サーバーやメンバー情報が読めなかったら無視
        return

    if member.bot: # BOTアカウントは無視する
        return

    if payload.channel_id != 123456789123: # 特定のチャンネル以外でリアクションを解除した場合は無視する
        return

    if payload.emoji.name == "👍": # 特定の絵文字
        await payload.member.remove_roles(
            payload.member.guild.get_role(123456789123) # ロールID
            )
  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    # channel_id から Channel オブジェクトを取得
    
    channel = self.bot.get_channel(payload.channel_id)

    # 該当のチャンネル以外はスルー
    if channel.id != self.ID_CHANNEL_README:
        return

    # guild_id から Guild オブジェクトを取得
    guild = self.bot.get_guild(payload.guild_id)

    # user_id から Member オブジェクトを取得
    member = guild.get_member(payload.user_id)

    # 用意した役職IDから Role オブジェクトを取得
    role = guild.get_role(self.ID_ROLE_WELCOME)

    # リアクションを付けたメンバーに役職を付与
    await member.add_roles(role)
    embed=discord.Embed(title="ロール付与",color=0xff0000)
    embed.add_field(name="内容", value=f"<@&{self.ID_ROLE_WELCOME}>を付与しました。",inline=False)
    await channel.send(embed=embed, delete_after=4.0)
  @commands.Cog.listener()
  async def on_raw_reaction_remove(self, payload):
      channel = self.bot.get_channel(payload.channel_id)

      # 該当のチャンネル以外はスルー
      if channel.id != self.ID_CHANNEL_README:
          return

      # guild_id から Guild オブジェクトを取得
      guild = self.bot.get_guild(payload.guild_id)

      # user_id から Member オブジェクトを取得
      member = guild.get_member(payload.user_id)

      # 用意した役職IDから Role オブジェクトを取得
      role = guild.get_role(self.ID_ROLE_WELCOME)

      # リアクションを付けたメンバーに役職を付与
      await member.remove_roles(role)
      embed=discord.Embed(title="ロール剥奪",color=0xff0000)
      embed.add_field(name="内容", value=f"<@&{self.ID_ROLE_WELCOME}>を剥奪しました。",inline=False)
      await channel.send(embed=embed, delete_after=4.0)

def setup(bot):
  return bot.add_cog(role_add(bot))