import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime
import pytz


class Users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        intents = discord.Intents.default()
        intents.members = True

    @commands.group()
    async def user(self, ctx):
        role = ctx.guild.get_role(813389100815351869)
        if ctx.author.guild_permissions.administrator or role in ctx.author.roles:
            if ctx.invoked_subcommand is None:
                await ctx.send('メインコマンドの後にサブコマンドが必要です。')

    @user.command(pass_context=True)
    async def dm(self, ctx, ids, word):
        user = discord.utils.get(self.bot.users, id=ctx)
        try:
            await user.send(f"{ctx.author.name}さんからDMが届きました。\nメッセージ内容\n{word}")
        except AttributeError:
            return ctx.send("そのユーザーは存在しません。\nBotが導入されているサーバーに存在するかお確かめ下さい。")

    @user.command()
    async def info(self, ctx, member: discord.Member):
        users = discord.Embed(title=f'{member}の詳細',
                              description='詳細',
                              color=discord.Color.orange())
        users.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        users.set_thumbnail(url=member.avatar_url)
        users.add_field(
            name='名前',
            value=f'**{member.display_name}#{member.discriminator}**')
        users.add_field(name='あなたはBot?', value=member.bot)
        users.add_field(name='作成時間', value=member.created_at, inline=False)
        users.add_field(name='サーバーに参加した時間', value=member.joined_at)
        await ctx.send(embed=users)

    @user.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason=None):
        kick = discord.Embed(title='メンバーをキックしました',
                             description='Kickしたメンバーにまた来てもらうには再招待してください',
                             color=discord.Color.red())
        kick.add_field(name='執行人', value=f'{ctx.author.mention}')
        kick.add_field(name='Kickされた人', value=f'{member.mention}')
        kick.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=kick)
        await member.kick(reason=reason)

    @user.command()
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, name):
        ban = discord.Embed(title='メンバーをBANしました',
                            description='BANしたメンバーにまた来てもらうにはUNBANをし再招待してください',
                            color=discord.Color.red())
        ban.add_field(name='執行人', value=f'{ctx.author.mention}')
        ban.add_field(name='Kickされた人', value=f'{member.mention}')
        ban.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=ban)
        await member.ban(reason=name)

    @user.command()
    @commands.has_permissions(ban_members=True)
    async def unban(ctx, member: discord.Member, reason=None):
        user = ['cogs.userinfocog']
        unban = discord.Embed(title="BANを解除しました", color=0xff0000)
        unban.set_thumbnail(url=user.avatar_url)
        unban.add_field(name="対象", value=user, inline=False)
        unban.add_field(name="実行", value=ctx.author, inline=False)
        await user.unban()
        await ctx.channel.send(embed=unban)

    @user.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, reason=None):
        guild = self.bot.get_guild(774477394924666890)
        role = guild.get_role(820072014185627648)
        await member.add_role(role)

    @commands.command(name="time")
    async def time(self, ctx):
        realtime = datetime.now(
            pytz.timezone('Asia/Tokyo')).strftime('%D:%H:%M')
        year = datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y')
        await ctx.send("今の時刻は" + year + "年の" + realtime + "だよ！")


def setup(bot):
    bot.add_cog(Users(bot))
