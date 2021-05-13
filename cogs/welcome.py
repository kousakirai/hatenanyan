from discord.ext import commands
import discord

class join(commands.Cog):
    """These are the developer commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member):
        print('ok')
        gil_join=discord.Embed(title='入室通知',description=f'{member.mention}が入室しました', color=0x3498db)
        #
        gil_join.set_thumbnail(url=f'{member.avatar_url}')
        await member.send("ただいまbot整備中※このDMは無視してかまいません")
        await member.guild.system_channel.send(embed=gil_join)  

def setup(bot):
	return bot.add_cog(join(bot))