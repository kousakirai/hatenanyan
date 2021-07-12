import os
import requests
import discord
from discord.ext import commands
from pprint import pprint
import aiohttp 

TOKEN= my_secret = os.environ['TOKEN']


AuthB = "Bot " + TOKEN

headers = {
    "Authorization": AuthB
}

def returnNormalUrl(channelId):
    return "https://discordapp.com/api/channels/" + str(channelId) + "/messages"


async def notify_callback(id, token):
    url = "https://discord.com/api/v8/interactions/{0}/{1}/callback".format(id, token)
    json = {
        "type": 6
    }
    async with aiohttp.ClientSession() as s:
        async with s.post(url, json=json) as r:
            if 200 <= r.status < 300:
                return


def normalMessage(msg, content):
    normal_url = returnNormalUrl(msg["d"]["channel_id"])
    json = {
        "content": content
    }
    r = requests.post(normal_url, headers=headers, json=json)


async def on_socket_response(msg):
    if msg["t"] != "INTERACTION_CREATE":
        return

    pprint(msg)
    custom_id = msg["d"]["data"]["custom_id"]

    if custom_id == "click_one":
        normal_url2 = returnNormalUrl(msg["d"]["channel_id"]) + "/" + msg["d"]["message"]["id"]
        json2 = {
            "content": "パー",
            "components": [
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 2,
                            "label": "グー",
                            "style": 1,
                            "custom_id": "click_one",
                            "disabled": False
                        },
                        {
                            "type": 2,
                            "label": "チョキ",
                            "style": 3,
                            "custom_id": "click_two",
                            "disabled": False
                        },
                        {    
                            "type": 2,
                            "label": "パー",
                            "style": 3,
                            "custom_id": "click_three",
                            "disabled": False
                        },
                    ]
                }
            ]
        }
        r2 = requests.patch(normal_url2, headers=headers, json=json2)
        pprint(r2)
        await notify_callback(msg["d"]["id"], msg["d"]["token"])
    elif custom_id == 'click_two':
        normal_url2 = returnNormalUrl(msg["d"]["channel_id"]) + "/" + msg["d"]["message"]["id"]
        json2 = {
            "content": "グー",
            "components": [
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 2,
                            "label": "グー",
                            "style": 1,
                            "custom_id": "click_one",
                            "disabled": False
                        },
                        {
                            "type": 2,
                            "label": "チョキ",
                            "style": 3,
                            "custom_id": "click_two",
                            "disabled": False
                        },
                        {
                            "type": 2,
                            "label": "パー",
                            "style": 3,
                            "custom_id": "click_three",
                            "disabled": False
                        },
                    ]

                }
            ]
        }
        r2 = requests.patch(normal_url2, headers=headers, json=json2)
        pprint(r2)
        await notify_callback(msg["d"]["id"], msg["d"]["token"])
    elif custom_id == 'click_three':
        normal_url2 = returnNormalUrl(msg["d"]["channel_id"]) + "/" + msg["d"]["message"]["id"]
        json2 = {
            "content": "チョキ",
            "components": [
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 2,
                            "label": "グー",
                            "style": 1,
                            "custom_id": "click_one",
                            "disabled": False
                        },
                        {
                            "type": 2,
                            "label": "チョキ",
                            "style": 3,
                            "custom_id": "click_two",
                            "disabled": False
                        },
                        {
                            "type": 2,
                            "label": "パー",
                            "style": 3,
                            "custom_id": "click_three",
                            "disabled": False
                        },
                    ]

                }
            ]
        }
        r2 = requests.patch(normal_url2, headers=headers, json=json2)
        pprint(r2)
        await notify_callback(msg["d"]["id"], msg["d"]["token"])

class MyBot(commands.Bot):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_listener(on_socket_response)


bot = MyBot(command_prefix='$', description='slash test')

class Mybot(commands.Cog):
    def __init__(self,bot, **kwargs):
      self.bot=bot


    @commands.Cog.listener()
    async def on_message(self,msg):
        if msg.content == "hello":
            print('ok')
            normal_url = returnNormalUrl(msg.channel.id)
            json = {
                "content": "じゃんけん",
                "components": [
                      {
                        "type": 1,
                        "components": [
                            {
                                "type": 2,
                                "label": "グー",
                                "style": 1,
                                "custom_id": "click_one",
                                "disabled": True
                            },
                            {
                                "type": 2,
                                "label": "チョキ",
                                "style": 1,
                                "custom_id": "click_two"
                            },
                                                    {
                                "type": 2,
                                "label": "パー",
                                "style": 1,
                                "custom_id": "click_three"
                            },
                        ]

                    }
                ]
            }
            r = requests.post(normal_url, headers=headers, json=json)

def setup(bot):
    return bot.add_cog(Mybot(bot))