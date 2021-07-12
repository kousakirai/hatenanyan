@slash.slash(name="set", guild_ids=guild_ids)
async def add(ctx):
    if len(db.search(User.name == ctx.author.id)) > 0:

        embed1 = discord.Embed(title="通貨システム", description=' ')
        embed1.add_field(name="あなたはすでに登録しています。", value='登録する必要はありません')

        await ctx.send(embed=embed1)
        return

    else:
        db.insert({'name': ctx.author.id, 'money': 200})

        embed2 = discord.Embed(title="通貨システム", description=" ")
        embed2.add_field(name="ユーザー情報を登録しました。", value="登録記念に100ニャンコインを贈呈します")
        await ctx.send(Embed=embed2)


@slash.slash(name="money", guild_ids=guild_ids)
async def money(ctx):
    if not len(db.search(User.name == ctx.author.id)) > 0:
        await ctx.send(content="ユーザー情報が確認できませんでした。\n/setを実行してください。")
    else:
        a = db.search(User.name == ctx.author.id)
        l = int(a[0]["money"]) / 2
        await ctx.send(content=f'{l}ニャンコインです')


@slash.slash(name="shop", guild_ids=guild_ids)
async def sp(ctx):
    embed = discord.Embed(title='A', description='a')
    await ctx.send(embed=embed)

@slash.slash(name="trans",description="google翻訳をしてくれるコマンドです。",guild_ids=guild_ids)
async def trans(ctx, word, lang=None):
    g = async_google_trans_new.AsyncTranslator()
    if lang is None:
        if (await g.detect(word))[0] == "ja":
            t = "en"
        else:
            t = "ja"
    else:
        t = lang
    result = await g.translate(word, t)
    embed = discord.Embed(title="google translate", color=0x00bfff)
    embed.add_field(name="before", value=word, inline=False)
    embed.add_field(name="after", value=result, inline=False)
    embed.set_footer(text="Powered by googletranslate",
                     icon_url="https://ssl.gstatic.com/translate/favicon.ico")
    await ctx.send(embed=embed, hidden=True)