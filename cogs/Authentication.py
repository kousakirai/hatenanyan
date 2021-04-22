import discord
from discord.ext import commands
import json
class Authentication(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    intents = discord.Intents.default()
    intents.members = True  
  def image_crete(self, ctx):
    import PIL.Image
    import PIL.ImageDraw
    import PIL.ImageFont

    # 使うフォント，サイズ，描くテキストの設定
    ttfontname = "cogs/NikkyouSans-mLKax.ttf"
    fontsize = 36
    text = "暗黙の型宣言"

    # 画像サイズ，背景色，フォントの色を設定
    canvasSize    = (300, 150)
    backgroundRGB = (255, 255, 255)
    textRGB       = (0, 0, 0)

    # 文字を描く画像の作成
    img  = PIL.Image.new('RGB', canvasSize, backgroundRGB)
    draw = PIL.ImageDraw.Draw(img)

    # 用意した画像に文字列を描く
    font = PIL.ImageFont.truetype(ttfontname, fontsize)
    textWidth, textHeight = draw.textsize(text,font=font)
    textTopLeft = (canvasSize[0]//6, canvasSize[1]//2-textHeight//2) # 前から1/6，上下中央に配置
    draw.text(textTopLeft, text, fill=textRGB, font=font)

    img.save("image.png")
  @commands.Cog.listener(name="on_member_join")
  async def on_member_join(self, ctx, member: discord.Member):
    await self.image_crete()
    await ctx.send(file=discord.File("image.png"))