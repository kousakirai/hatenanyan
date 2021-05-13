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
    #===== global =====#
    self.config = configparser.SafeConfigParser()
    self.config.read('option.ini', encoding = 'utf8')
    self.GAME = discord.Game(name = "OneNightJinro")
    self.CHANNEL = None#discord.channel(id=config["BOT"]["CHANNEL"])
    self.STARTED = False
    self.PLAYING = False
    self.validate = None
    self.STATEMENT = "hoge"
    self.send = Queue()
    self.receive = Queue()
    #receive for discord to game, send for game to discord


  

  #===== gameplay =====#
  players = []

  #===== script =====#

  #===== bot =====#
  @commands.Cog.listener()
  async def on_ready(self):
    global CHANNEL
    CHANNEL = self.bot.get_channel(int(self.config["BOT"]["CHANNEL"]))
  @commands.group()
  async def wolf(self, ctx):
      if ctx.invoked_subcommand is None:
          await ctx.send('メインコマンドの後にサブコマンドが必要です。')
  @wolf.command()
  async def start(self, ctx):
      global STARTED
      global PLAYING # thanks to @2103Kuchinashi
      global CHANNEL
      global validate
      global players
      if not STARTED:
          await CHANNEL.send("ワンナイト人狼ゲームを始めます。")
          await self.bot.change_presence(activity = self.GAME)
          await CHANNEL.send('参加したい人は"/join"と入力。')
          await CHANNEL.send('全員の入力が終わったら"/go"と入力。')
          STARTED = True
  @wolf.command()
  async def join(self, ctx):
    global STARTED
    global PLAYING # thanks to @2103Kuchinashi
    global CHANNEL
    global validate
    global players
    if not PLAYING and STARTED:
        p = []
        for player in players:
            p.append(player.discord)
        if ctx.author in p:
            await CHANNEL.send("{} はもう登録済みです。".format(ctx.author.name))
        else:
            hoge = self.Player(ctx)
            players.append(hoge)
            await CHANNEL.send("{} を登録しました。".format(self.send.get()))
  @wolf.command()
  async def go(self, ctx):
    global STARTED
    global PLAYING # thanks to @2103Kuchinashi
    global CHANNEL
    global validate
    global players
    if len(players)<3:
        await CHANNEL.send("3人以上いないとプレイできません。再度/startからやりなおしてください。")
    else:
        PLAYING = True
        await CHANNEL.send("全員の準備が完了しました。夜のアクションに入ります。\nアクションはDMで行います。")
        deck = self.makeDeck(len(players))
        playable, remaining = self.decideRole(deck)
        for x, player in enumerate(players):
            player.role = playable[x]

        for player in players:
            await player.discord.send('{} のターンです。'.format(player.name))
            act = Thread(target = player.action, args = (players,remaining,), name = "act")
            act.start()
            while True:
                  state = self.send.get()
                  if state[0] == "end":
                      await player.discord.send(state[1])
                      break
                  elif state[0] == "exc":
                      await player.discord.send(state[1])
                  else:
                      await player.discord.send(state[1])
                      validate = player.discord
                      message = await self.bot.wait_for("message", check=self.wait_for_player)
                      self.receive.put(ctx)

        players = self.swapRobber(players)
        await CHANNEL.send('全員のアクションが完了したので、誰を処刑するか話し合いを始めてください。\n話し合いが終わったら"/ready"と入力。')
        message = await self.bot.wait_for('ctx', check=self.wait_for_ready)

        await CHANNEL.send('それでは、投票に入ります。\n投票もDMで行います。')
        for player in players:
            v = Thread(target = self.vote, args = (player, players, remaining,),name = "vote")
            v.start()
            while True:
                state = self.send.get()
                if state[0] == "end":
                    await player.discord.send(state[1])
                    break
                elif state[0] == "exc":
                    await player.discord.send(state[1])
                else:
                    await player.discord.send(state[1])
                    validate = player.discord
                    message = await self.bot.wait_for("message", check=self.wait_for_player)
                    self.receive.put(message.content)
                results = self.getVoteResult(players, playable)
                await CHANNEL.send('全員の投票が終わりました。')
                await CHANNEL.send(self.send.get())
                await CHANNEL.send('それでは、結果発表です。')
                getres = Thread(target = getGameresult, args = (players, results, remaining,), name = "getres")
                getres.start()
                while True:
                    state = self.send.get()
                    if state[0] == "end":
                        await CHANNEL.send(state[1])
                        break
                    else:
                        await CHANNEL.send(state[1])
            STARTED = False
            PLAYING = False
            players = []
            await CHANNEL.send('"/start" で次のゲームを開始します。\n"/shutdown"で終了します。')

  #===== supporting functions =====#
  def wait_for_ready(message):
      return message.channel==CHANNEL and message.content=="/ready"

  def wait_for_player(message):
      return message.author==validate

  #===== JinroGame =====#
  class Player():
      def __init__(self, discord):
          self.role = ""
          self.type = ""
          self.robberflag = False
          self.robberbuff = ""
          self.discord = discord
          self.name = self.discord.name
          self.voted = 0
          self.send.put(self.name)

      def action(self, players, remaining):
          if self.role == "seer":
              self.send.put(["/seer", 'あなたは##### seer #####です。\n\n占いをするか、残りの2枚のカードを見るか選択してください。\n1 占う\n2 カードを見る'])#\n\n返答は"/seer [content]"のフォーマットで行ってください。'])
              while True:
                  choice = self.receive.get()
                  if choice not in ["1", "2"]:
                      self.send.put(["exc", "入力が正しくありません。"])
                  else:
                      choice = int(choice)
                      break

              if choice == 1:
                  tmp = []
                  sentence = "占いたい人の番号を入力してください。\n"
                  for i, player in enumerate(players):
                      if player.name == self.name:
                          None
                      else:
                          sentence += (str(i+1) + " " + player.name + "\n")
                          tmp.append(str(i+1))
                  self.send.put(["/seer", sentence])
                  while True:
                      target = self.receive.get()
                      if target is None:
                          None
                      elif target in tmp:
                          target = int(target) - 1
                          self.send.put(["end", players[target].name + " を占ったところ、 " + players[target].role + " だとわかりました。\n\nこれであなたのアクションは完了しました。"])
                          break
                      else:
                          self.send.put(["exc", "入力が正しくありません。"])

              elif choice == 2:
                  sentence = "残りの2枚のカードは、" + str(remaining) + "です。\n\nこれであなたのアクションは完了しました。"
                  self.send.put(["end", sentence])


          elif self.role == "werewolf":
              self.send.put(["/werewolf", "あなたは##### werewolf #####です。\n仲間を確認するため、カモフラージュも兼ねて何か適当に入力してください。\n"])
              lonely = True
              sentence = ""
              for player in players:
                  if player.role == "werewolf":
                      if not player.name == self.name:
                          sentence += ("werewolf: " + player.name + "\n")
                          lonely = False
              if lonely:
                  sentence = "仲間はいないようだ。\n"
              hoge = self.receive.get()
              sentence += "\nこれであなたのアクションは完了しました。"
              self.send.put(["end", sentence])


          elif self.role == "robber":
              sentence = "あなたは##### robber #####です。\n役職を交換したいプレイヤーの番号を入力してください。\n"
              tmp = []
              for i, player in enumerate(players):
                  if player.name == self.name:
                      None
                  else:
                      sentence += (str(i+1) + " " + player.name + "\n")
                      tmp.append(str(i+1))
              self.send.put(["/robber", sentence])
              while True:
                  target = self.receive.get()
                  if target is None:
                      None
                  elif target in tmp:
                      target = int(target) - 1
                      newrole = players[target].role
                      players[target].robberflag = True
                      self.robberflag = True
                      self.robberbuff = newrole
                      self.send.put(["end", players[target].name + " からカードを奪い、あなたは " + newrole + " になりました。\nこのことは相手には通知されません。\n\nこれであなたのアクションは完了しました。"])
                      break

                  else:
                      self.send.put(["exc", "入力が正しくありません。"])


          elif self.role == "hangman":
              self.send.put(["/hangman", "あなたは##### hangman #####です。\nやることはないので、カモフラージュのために何か適当に打ち込んでください。"])
              hoge = self.receive.get()
              self.send.put(["end", "\nこれであなたのアクションは完了しました。"])

          elif self.role == "villager":
              self.send.put(["/villager","あなたは##### villager #####です。\nやることはないので、カモフラージュのために何か適当に打ち込んでください。"])
              hoge = self.receive.get()
              self.send.put(["end", "\nこれであなたのアクションは完了しました。"])

      def killed(self, players, playable):#returnは勝利プレイヤーの属性
        if self.role == "hangman":
            return "hangman"
        elif self.role == "werewolf":
            return "villager"
        elif "werewolf" not in playable:
            return "nobody"
        else:
            return "werewolf"

  def makeDeck(self, num_player):
      num_player = int(num_player)
      deck = []
      role = []
      roles = self.config["roles{}".format(num_player)]
      for i in roles:
          role.append(i)
      for i in role:
          a = int(roles[i])
          for j in range(a):
            deck.append(i)
      return deck

  def decideRole(deck):
      random.shuffle(deck)
      playable = deck[:-2]
      remaining = deck[-2:]

      return playable, remaining

  def swapRobber(players):
      for player in players:
          if player.robberflag == True:
              if player.role == "robber":
                  player.role = player.robberbuff
              else:
                  player.role = "robber"

      return players

  def vote(self, player, players, playable):
      sentence = player.name + " さんの投票です。\n投票したいプレイヤーの番号を入力してください。\n"
      tmp = []
      for x, i in enumerate(players):
          if player.name != i.name:
              sentence += (str(x+1) + " " + i.name + "\n")
              tmp.append(str(x+1))

      self.send.put(["/vote", sentence])
      while True:
          tar = self.receive.get()
          if tar.isdigit() and tar in tmp:
              players[int(tar)-1].voted += 1
              self.send.put(["end", players[int(tar)-1].name+" に投票しました。"])
              break
          else:
              self.send.put(["exc", "入力が正しくありません。"])

  def getVoteResult(self, players, playable):
      judge = []
      names = []
      most = players[0].voted
      for player in players:
          if player.voted == most:
              judge.append(player)
              names.append(player.name)
          elif player.voted > most:
              judge = []
              names = []
              judge.append(player)
              names.append(player.name)
              most = player.voted

      if len(names) == len(players):
          self.send.put("あなたたちは平和村を宣言しました。")
          if "werewolf" in playable:
              return ["werewolf"]
          else:
              return ["peaceful"]

      self.send.put("投票の結果、処刑されるプレイヤーは " + str(names) + " です。")
      results = []
      for i in judge:
          results.append(i.killed(players, playable))
      return results

  def judgement(self, players, playable):#投票なしの場合(ボツ)
      sentence = "\nそれでは、処刑するプレイヤーの番号を入力してください。\n平和村だと思う場合は、0を入力してください。\n\n"
      sentence += "0 平和村宣言\n"
      for i, player in enumerate(players):
          sentence += (str(i+1) + " " + player.name + "\n")
      while True:
          judge = self.receive.get()
          if judge is None:
              None
          elif judge == "0":
              self.send.put(["end","あなたたちは平和村を宣言しました。"])
              if "werewolf" not in playable:
                  return "peaceful"
              else:
                  return "werewolf"
          elif judge not in range(len(players)+1):
              self.send.put(["exc", "入力が正しくありません。"])
          else:
              self.send.put(["end", players[int(judge)-1].name + " を処刑します。"])
              result = players[int(judge)-1].killed(players, playable)
              break
      return result

def getGameresult(self, players, results, remaining):
    sentence = ""
    sleep(7)#ドキドキ感の演出
    if "hangman" in results:
        self.send.put([" ", "### 吊り人 ### の勝利です。\n\n勝利プレイヤー\t役職"])
        for player in players:
            if player.role == "hangman":
                sentence += (player.name + "\t" + player.role + "\n")

    elif "villager" in results:
        self.send.put([" ", "### 市民チーム ### の勝利です。\n\n勝利プレイヤー\t役職"])
        for player in players:
            if player.role not in ["hangman", "werewolf"]:
                sentence += (player.name + "\t" + player.role + "\n")

    elif "werewolf" in results:
        self.send.put([" ", "### 人狼チーム ### の勝利です。\n\n勝利プレイヤー\t役職"])
        for player in players:
            if player.role == "werewolf":
                sentence += (player.name + "\t" + player.role + "\n")

    elif "peaceful" in results:
        sentence = "### 平和村 ### でした。\n"

    elif "nobody" in results:
        sentence = "### 勝者なし ###\n"

    sentence += "\n\n各プレイヤーの役職は以下の通りでした。\n"
    for i, player in enumerate(players):
        sentence += (player.name + "\t" + player.role + "\n")
    sentence += ("\nそして、残っていた2枚のカードは" + str(remaining) + "でした。\n\nお疲れさまでした。")
    self.send.put(["end", sentence])
  

def setup(bot):
  return bot.add_cog(wolfsystems(bot))