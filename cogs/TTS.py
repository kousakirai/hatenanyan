import discord
from gtts import gTTS 
from discord.ext import commands
flag = 0
class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    def voice_generator(self,message):
        storepath = "C:/pythontest/"
        language ='ja'
        output = gTTS(text=message, lang=language, slow=False)
        storepath = "C:/voice/"
        voice_folder = storepath + f"{message.author}voice_output.mp3"
        output.save(voice_folder)
        return voice_folder
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.voice is None:
            return
        if message.author.bot:
            return
        if flag == 1:
            reading_voice = self.voice_generator(message)
            await message.guild.voice_client.play(reading_voice)
        else:
            return
    @commands.group()
    async def yomi(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply("サブコマンドが存在しません。")
    @yomi.command()
    async def join(self, ctx):
        """
      botを現在入っているボイスチャンネルに呼び出します。
      """
        if ctx.author.voice is None:
            await ctx.channel.send("あなたはボイスチャンネルに接続していません。")
            return
        # ボイスチャンネルに接続する
        await ctx.author.voice.channel.connect()
        await ctx.send("接続しました。")

    @yomi.command()
    async def leave(self, ctx):
        """
      Botをボイスチャンネルから離脱させます。
      """
        if ctx.guild.voice_client is None:
            await ctx.send("接続していません。")
            return
        if ctx.guild.voice_client.is_playing():
            await ctx.send("再生中です。")
            return
        self.d.clear()
        await ctx.guild.voice_client.disconnect()
        await ctx.send("切断しました。")

def setup(bot):
    return bot.add_cog(TTS(bot))
    