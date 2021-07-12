from discord.ext import commands, tasks
import discord
import asyncio
import os
from discord.ext.commands import CommandNotFound, CommandOnCooldown


class weakup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=5)
    async def aaaaa(self):
        guild = self.bot.get_guild(774477394924666890)
        await self.bot.change_presence(
            activity=discord.Game(len(guild.members)))
        await asyncio.sleep(10)
        await self.bot.change_presence(
            activity=discord.Game(f'{len(guild.members)}人'))
        await asyncio.sleep(10)

    @commands.Cog.listener()
    async def on_ready(self):
        print('起動中です...')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('おはようございますマスター！()')
        channel = self.bot.get_channel(818817278912626718)
        cogs = [
            f"cogs.{path[:-3]}" for path in os.listdir('./cogs')
            if path.endswith('.py')
        ]
        self.bot.load_extension("adminonly.debug")
        self.bot.load_extension("cogs.level")
        self.aaaaa.start()

        for cog in cogs:
            self.bot.load_extension(cog)

        await channel.send(
            "```疑問猫Bot再起動しました。起動時になにかエラーが起きた場合は制作者のkousakiraiにお伝え下さい。社畜のように働きます()```"
        )


def setup(bot):
    return bot.add_cog(weakup(bot))
