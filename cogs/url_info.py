'''
できた
動作未確認
気になるのがulangの部分がjpnでエラー起きてる
シングルクォーテーションつけなくていいのだろうか...
ありがとう修正した
動作確認お願い
'''
from discord.ext import commands
import discord
from bs4 import BeautifulSoup
import requests
import re
import io
from urllib.parse import urlparse


class Safe_web(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def url_info(self, ctx, url=None):
        embed = discord.Embed(title="解析中")
        m = await ctx.send(embed=embed)
        query = {"url": url, "ulang": "jpn"}
        res = requests.get("https://safeweb.norton.com/report/show",
                           params=query)
        soup = BeautifulSoup(res.text, 'html.parser')
        try:
            if soup.b.string == "安全":
                print("安全です。")
                embed = discord.Embed(
                    title='安全',
                    description=f'ノートン セーフウェブが`{url}`を分析して安全性とセキュリティの問題を調べました。',
                    color=0x3498db)
                embed.set_footer(text="Powered by norton safeweb")
                await m.edit(embed=embed)
            elif soup.b.string == "注意":
                print("注意")
                embed = discord.Embed(
                    title="注意",
                    description=
                    "［注意］の評価を受けた Web サイトは少数の脅威または迷惑を伴いますが、赤色の［警告］に相当するほど危険とは見なされません。サイトにアクセスする場合には注意が必要です。",
                    color=0x3498db)
                embed.set_footer(text="Powered by norton safeweb")
                await m.edit(embed=embed)
            elif soup.b.string == "警告":
                print("警告")
                embed = discord.Embed(
                    title="警告",
                    description="これは既知の危険な Web ページです。このページを開かないことを推奨します。")
                embed.set_footer(text="Powered by norton safeweb")
                await m.edit(embed=embed)
            else:
                embed = discord.Embed(title="未評価", description="評価されていません。")
                embed.set_footer(text="Powered by norton safeweb")
                await m.edit(embed=embed)
        except:
            print("error")
            embed = discord.Embed(
                title="エラー", description="エラーが発生しました。urlに誤りがないかもう一度確かめてください。")
            embed.set_footer(text="Powered by norton safeweb")
            await m.edit(embed=embed)
            
    @commands.Cog.listener()
    async def on_message(self, message):
      if message.author.bot:
        return
      pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
      url_list = re.findall(pattern, message.content)
      site = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(url_list[0]))
      query = {
        "url": site,
        "ulang": "jpn"
      }
      res = requests.get("https://safeweb.norton.com/report/show",params=query)
      print(res.text)
      soup = BeautifulSoup(res.text, 'html.parser')
      if soup.b.string == "安全":
        await message.add_reaction("✅")
      else:
        ch_webhooks = await message.channel.webhooks()
        webhook = discord.utils.get(ch_webhooks, name="hatena-tool")
        if webhook is None:
          webhook = await message.channel.create_webhook(name="hatena-tool")
        await message.delete()
        fl=[]
        for at in message.attachments:
          fl.append(await at.to_file())
        await webhook.send(content=f"{message.clean_content} ({soup.b.string})", username=f"{message.author} ({message.author.id})", avatar_url=message.author.avatar.url)


def setup(bot):
    bot.add_cog(Safe_web(bot))
