import discord
from discord.ext import commands, tasks
from datetime import datetime


class Twitter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


@commands.command(name="Twitter")
async def Twi(self, ctx):
    GLOBAL_CH_NAME = "Twi-qs"
    GLOBAL_WEBHOOK_NAME = "Twitter発信くん"  # グローバルチャットのWebhook名
    channels = self.bot.get_all_channels()
    global_channels = [ch for ch in channels if ch.name == GLOBAL_CH_NAME]
    for channel in global_channels:
        ch_webhooks = await self.bot.channel.webhooks()
        webhook = discord.utils.get(ch_webhooks, name=GLOBAL_WEBHOOK_NAME)
        if webhook is None:
            # そのチャンネルに hoge-webhook というWebhookは無かったので無視
            return
        await webhook.send()


def setup(bot):
    return bot.add_cog(Twitter(bot))
