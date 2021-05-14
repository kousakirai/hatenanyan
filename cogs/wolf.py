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
    

def setup(bot):
  return bot.add_cog(wolfsystems(bot))