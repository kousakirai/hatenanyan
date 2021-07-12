import discord
from discord.ext import commands
from time import sleep
from threading import Thread
from queue import Queue
import configparser
import random


class wolfsystems(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.on_playerlist = []
        self.game = 0

    @commands.command()
    async def make(self, ctx):
        if self.game in 1:
            await ctx.send("すでにゲームが進行、作成されています。")
        self.game = 1
        await ctx.send("人狼ゲームを作成しました。")

    @commands.command()
    async def join(self, ctx):
        if self.game in 0:
            await ctx.send("ゲームに参加しようとしましたが見つかりませんでした。")
        if ctx.author.id in self.on_playerlist:
            await ctx.send("あなたはすでにゲームに参加しています。")
        self.on_playerlist.append(ctx.aurhor.id)
        await ctx.send("人狼ゲームに参加しました。")
    @commands.command()
    async def start(self, ctx):
        for a in self.on_playerlist:
            if a <4:
                await ctx.send("ゲームに参加する人数が不足しています。")
        self.game = 1
        await ctx.send("それではゲームを開始します。")
        

def setup(bot):
    return bot.add_cog(wolfsystems(bot))