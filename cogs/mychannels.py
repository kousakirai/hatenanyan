import discord
from discord.ext import commands


class my(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mychannel", aliases=["myc"])
    async def mychannel(self, ctx, ch_name):
        category = ctx.guild.get_channel(844541284727259147)
        await category.create_text_channel(name=ch_name)
        await ctx.reply(f"{ch_name}を作成しました。")


def setup(bot):
    return bot.add_cog(my(bot))
