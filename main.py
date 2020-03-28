import discord

from random import random
from discord.ext import commands
from Embeds.Embeds import embed_help
from SRC.reddit import gather_post_info, upvotes, titles, pictures, links
from SRC.utilites import get_gif, get_random_gif, output_random_quote

gif_api_key = "89HJRRKY8549"
client = commands.Bot(command_prefix="!ye ")
client.remove_command("help")
list_of_commands = [['help', "Shows list of commands"],
                    ['play {album] or {link} or {song}', "Plays the desired song/album"],
                    ['gif', "Shows random Kanye gif"],
                    ['subreddit', "Shows top 5 r/Kanye posts"],
                    ['quote', "Shows random quote"],
                    ['god', "Shows random Kanye god gif"],
                    ['kobe', "Shows legendary Kanye + Kobe video"]]


@client.command()
async def help(ctx):
    await ctx.send(embed=embed_help(list_of_commands))


@client.command()
async def play(ctx):
    pass


@client.command()
async def gif(ctx):
    list = get_random_gif()
    for response in list['results']:
        await ctx.send(response["url"])


@client.command()
async def subreddit(ctx):
    await ctx.send(f"One moment {ctx.author}")
    gather_post_info()
    index = 0
    while index < 5:
        embed = discord.Embed(color=0xff0000)
        if index == 4:
            embed.set_image(url="https://thumbs.gfycat.com/HatefulClutteredIrishwolfhound-size_restricted.gif")
        else:
            embed.set_image(url=pictures[index])
        embed.add_field(name=f"#{index + 1}  -  <:upvote:692958740865089536> {upvotes[index]} Upvotes",
                        value=f"[{titles[index]}]({links[index]})", inline=False)
        await ctx.send(embed=embed)
        index += 1


@client.command()
async def quote(ctx):
    random_quote = output_random_quote()[random.randint(0, 25)]
    await ctx.send("\"" + random_quote.strip("\n") + "\"")


@client.command()
async def god(ctx):
    await ctx.send("https://tenor.com/view/kanye-agod-iam-agod-kanye-west-conceited-gif-5313292")


@client.command()
async def kobe(ctx):
    await ctx.send("https://youtu.be/uxgHmbM3Ig0")


@client.event
async def on_ready():
    print("The bot is ready!")
    await client.change_presence(activity=discord.Game(name='Listening to YEEZUS'))


client.run('NjkyNTc2MTcxOTAwMTQxNTk4.Xn-F3Q.ydOaSVU-5N2nl5bO6PJOGTPN3j8')
