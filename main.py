import json
import discord
from pip._vendor import requests
from Embeds.Embeds import embed_help
import random


gif_api_key = "89HJRRKY8549"
client = discord.Client()
syntax = '!ye '
list_of_commands = [['help', "Shows list of commands"],
                   ['play {album] or {link} or {song}', "Plays the desired song/album"],
                   ['gif', "Shows random Kanye gif"],
                   ['subreddit ', "Shows top 5 r/Kanye posts"],
                   ['god', "Shows random Kanye god gif"],
                   ['kobe', "Shows legendary Kanye + Kobe video (rip :()"]]


def format_command(command):
    return f'{syntax}' + command


def get_gif(name):
    pos = "6"
    r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&pos=%s&limit=%s" % (name, gif_api_key, pos, 1))
    if r.status_code == 200:
        return json.loads(r.content)


def get_random_gif():
    pos = str(random.randint(0, 100))
    good_pos = False
    print(pos)

    while not good_pos:
        if pos == 99 or pos == 100 or pos == 50:
            pos = str(random.randint(0, 100))
        else:
            good_pos = True

    r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&pos=%s&limit=%s" % ("kanye", gif_api_key, pos, 1))
    if r.status_code == 200:
        return json.loads(r.content)


@client.event
async def on_ready():
    print("The bot is ready!")
    await client.change_presence(activity=discord.Game(name='Testing'))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content == syntax.replace(" ", "") or message.content == format_command('help'):
        await message.channel.send(embed=embed_help(list_of_commands))
    elif message.content == format_command('gif'):
        list = get_random_gif()
        for response in list['results']:
            await message.channel.send(response["url"])
    elif message.content == format_command('god'):
        await message.channel.send("https://tenor.com/view/kanye-agod-iam-agod-kanye-west-conceited-gif-5313292")
    elif message.content == format_command('kobe'):
        await message.channel.send("https://youtu.be/uxgHmbM3Ig0")

client.run('token')