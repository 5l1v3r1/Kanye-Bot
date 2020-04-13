import discord
import random
import os

from discord.ext import commands, tasks
from discord.utils import get

from Embeds.Embeds import embed_help
from SRC.reddit import gather_post_info, upvotes, titles, pictures, links
from SRC.utilites import get_random_gif, output_random_quote
from SRC.music import play_help_embed, YTDLSource, Music

music = None
client = commands.Bot(command_prefix="!ye ")
client.remove_command("help")
list_of_status = ["College Dropout", "Late Registration", "Graduation", "808s & Heartbreaks", "My Dark Fantasy",
                  "Watch The Throne", "YEEZUS", "The Life of Pablo", "Ye", "Kids See Ghosts", "Jesus Is King",
                  "Sunday Service"]
list_of_commands = [['help', "Shows list of commands"],
                    ['play {album] or {link} or {song}', "Plays the desired song/album"],
                    ['skip + or all', "Skips single song in queue or whole queue will 'all'"],
                    ['play help', "Shows help info"],
                    ['gif', "Shows random Kanye gif"],
                    ['subreddit', "Shows top 5 r/Kanye posts"],
                    ['quote', "Shows random quote"],
                    ['god', "Shows random Kanye god gif"],
                    ['familyfeud', "Shows family feud meme"],
                    ['kobe', "Shows legendary Kanye + Kobe video"],
                    ['thicc', 'Take a guess?'],
                    ['credits', "credits to the creator :D"]]


@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name=list_of_status[random.randint(0, 10)]))


@client.command(pass_context=True)
async def leave(ctx):
    for x in client.voice_clients:
        if x.channel == ctx.author.voice.channel:
            return await x.disconnect()


@client.command(pass_context=True, commands=["play help"])
async def play_help(ctx, command):
    if command == "help":
        await ctx.send(embed=play_help_embed)


@client.command(pass_context=True)
async def pause(ctx):
    if ctx.message.guild.voice_client is None:
        await ctx.send("No music playing to pause")
    ctx.message.guild.voice_client.pause()
    embed = discord.Embed(title="Paused")
    embed.set_thumbnail(url="https://media1.tenor.com/images/fdbdfca68e86c2580fd4bb155f95281f/tenor.gif?itemid=14908888")
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def resume(ctx):
    if ctx.message.guild.voice_client is None:
        await ctx.send("No music paused to resume")
    ctx.message.guild.voice_client.resume()
    embed = discord.Embed(title="Resumed")
    embed.set_thumbnail(url="https://media1.tenor.com/images/ba2a1aa852f101d2a0ddf523c876cfbf/tenor.gif?itemid=14908886")
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def skip(ctx, *, all=None):
    if all is None:
        await Music().skip(ctx)
    elif all == "all":
        await Music().skip(ctx, True)


@client.command(pass_context=True)
async def play(ctx, *, source=None, channel: discord.VoiceChannel = None):
    if source == "help":
        await ctx.send("No song/album/url specified!", embed=play_help_embed)
        return

    voice_client = get(client.voice_clients, guild=ctx.message.guild)

    try:
        if Music().server_music[ctx.message.guild.id] is None:
            Music().server_music[ctx.message.guild.id] = {'voice': voice_client, 'players': None}
    except KeyError:
        Music().server_music[ctx.message.guild.id] = {'voice': voice_client, 'players': None}

    # if no channel specified and user is not in voice channel
    if not channel and not ctx.author.voice:
        await ctx.send("Your not in a voice channel!")
        return

    url = None
    if not source:
        await ctx.send("No song/album/url specified!", embed=play_help_embed)
        return
    else:
        value = Music().get_source(source)
        if value is None:
            await ctx.send("Invalid song")
            return
        else:
            url = value

    # before connecting check if we already are
    if voice_client and voice_client.is_connected():
        # check for queue or if we're already playing a song
        players = Music().server_music[ctx.message.guild.id]['players']
        if players or voice_client.is_playing():
            await Music().add_to_queue(ctx, url)
            return
        else:  # no queue but connect, move to specified channel
            await voice_client.move_to(channel or ctx.author.voice.channel)
    else:  # not connected at all
        # connect
        destination = channel or ctx.author.voice.channel
        voice_client = await destination.connect()

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=client.loop, ctx=ctx)
        if player is None:
            return
        # rename file
        for file in os.listdir("./"):
            if file.endswith(".webm") or file.endswith(".m4a"):
                Music().server_file_names.append(file)
        voice_client.play(player, after=lambda e: client.loop.create_task(Music().play_next_song(ctx)))
        Music().server_music[ctx.message.guild.id] = {'voice': voice_client, 'players': [player]}
    await ctx.send(embed=Music().now_playing_embed(player.title))


@client.command(pass_context=True)
async def help(ctx):
    await ctx.send(embed=embed_help(list_of_commands))


@client.command(pass_context=True)
async def gif(ctx):
    await ctx.send(get_random_gif())


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
    random_quote = output_random_quote()[random.randint(0, 56)]
    await ctx.send("\"" + random_quote.strip("\n") + "\"")


@client.command(pass_context=True)
async def god(ctx):
    await ctx.send("https://tenor.com/view/kanye-agod-iam-agod-kanye-west-conceited-gif-5313292")


@client.command(pass_context=True)
async def kobe(ctx):
    await ctx.send("https://youtu.be/uxgHmbM3Ig0")\


@client.command(pass_context=True)
async def familyfeud(ctx):
    await ctx.send("https://www.youtube.com/watch?v=lE_QA6UqNhk")


@client.command(pass_context=True)
async def thicc(ctx):
    await ctx.send("https://gfycat.com/kindheartedgiantemperorshrimp")


@client.command(pass_context=True)
async def credits(ctx):
    embed = discord.Embed(title="The Creator", description="My creator is NMan4#6604, also known as Nick. The source code for this project is publicly available on my Github!")
    embed.set_author(name="NMan4#6604", url="https://github.com/NMan1/", icon_url = "https://i.imgur.com/IdUFBoP.jpg")
    embed.add_field(name="Source code:", value="https://github.com/NMan1/Kanye-Bot", inline=True)
    await ctx.send(embed=embed)


@client.event
async def on_ready():
    print("The bot is ready!", flush=True)
    change_status.start()


if __name__ == '__main__':
    Music().initialize_client(client)
    client.run("Njk2OTE2NjkyMzUzMTU1MTY0.XpC7XQ.2CqlGiO7qivSGWEWQ3P08nGZhSY")
