import discord
import random

from discord.utils import get
from discord.ext import commands, tasks
from Embeds.Embeds import embed_help
from SRC.reddit import gather_post_info, upvotes, titles, pictures, links
from SRC.utilites import get_gif, get_random_gif, output_random_quote
from SRC.music import play_help_embed, YTDLSource, now_playing_embed

client = commands.Bot(command_prefix="!ye ")
client.remove_command("help")
list_of_status = ["College Dropout", "Late Registration", "Graduation", "808s & Heartbreaks", "My Dark Fantasy",
                  "Watch The Throne", "YEEZUS", "The Life of Pablo", "Ye", "Kids See Ghosts", "Jesus Is King",
                  "Sunday Service"]
list_of_albums = ["college dropout", "collegedropout", "cd", "late registration", "lateregistration", "lr",
                  "graduation", "gr", "808s & heartbreaks", "808s and heartbreaks", "808's & heartbreaks",
                  "808's and heartbreaks", "808", "808s", "808's", "my beautiful dark twisted fantasy", "mbdtf",
                  "watch the throne", "wth", "yeezus", "the life of pablo", "tlop", "pablo", "ye", "kids see ghosts",
                  "ksg", "jesus is king", "jik", "sunday service", "ss"]
playlists_of_albums = ["https://www.youtube.com/watch?v=OTZzjAU0Kg0&list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh",
                       "https://www.youtube.com/watch?v=Bwyu-SZ7g_E&list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7",
                       "https://www.youtube.com/watch?v=JRnp5nwnkgI&list=PLXR4OlatIg5Fpc8HaoBlznnCGXMVJC9Ql",
                       "https://www.youtube.com/watch?v=d9BMPmfxaoM&list=PLX68ZEYlh74tpCb5sOXP98ito6DhP60-t",
                       "https://www.youtube.com/watch?v=UTH1VNHLjng&list=PLzMq4yH_FvVa5kPgtKmgdzPssfmBUtO2C",
                       "https://www.youtube.com/watch?v=FJt7gNi3Nr4&list=PLTI4-CRTcbtZup8J0WdvJm-JMgMJhnnOb",
                       "https://www.youtube.com/watch?v=uU9Fe-WXew4&list=PLzMq4yH_FvVaV0uPkc_Quj3PaXnpouNld",
                       "https://www.youtube.com/watch?v=6oHdAA3AqnE&list=PLzMq4yH_FvVac_1R0DMcMkcwnJ1-hFx6b",
                       "https://www.youtube.com/watch?v=2SeVgStQ5T0&list=PLAUxsgLNM2Bt8apMzywvdzOJSzlfW4OQa",
                       "https://www.youtube.com/watch?v=rnZQvgWhM5s&list=PLzMq4yH_FvVaq5TFtfCDs6FxWef45gyHW",
                       "https://www.youtube.com/watch?v=T58tRXzjC7c&list=PL5Z-QTr_hR1gTIk7T-bPCmRaaXNmiP3aK",
                       "https://www.youtube.com/watch?v=2Czs7fl1r7c&list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo"]
server_players = {}
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
    embed.set_thumbnail(
        url="https://media1.tenor.com/images/fdbdfca68e86c2580fd4bb155f95281f/tenor.gif?itemid=14908888")
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def resume(ctx):
    if ctx.message.guild.voice_client is None:
        await ctx.send("No music paused to resume")
    ctx.message.guild.voice_client.resume()
    embed = discord.Embed(title="Resumed")
    embed.set_thumbnail(
        url="https://media1.tenor.com/images/ba2a1aa852f101d2a0ddf523c876cfbf/tenor.gif?itemid=14908886")
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def play(ctx, *, source=None, channel: discord.VoiceChannel = None):
    if not channel and not ctx.author.voice:
        await ctx.send("Your not in a voice channel!")
    else:
        if not source:
            await ctx.send("No song/album/url specified!", embed=play_help_embed)
        else:
            if source.find("https") != -1:
                source = source
            elif source in list_of_albums:
                index = list_of_albums.index(source)
                if index < 3:
                    source = playlists_of_albums[0]
                elif index < 6:  # college dropout
                    source = playlists_of_albums[1]
                elif index < 8:  # late regestraration
                    source = playlists_of_albums[2]
                elif index < 15:  # graduation
                    source = playlists_of_albums[3]
                elif index < 15:  # 808's
                    source = playlists_of_albums[4]
                elif index < 17:  # MBDTF
                    source = playlists_of_albums[5]
                elif index < 19:  # Watch the throne
                    source = playlists_of_albums[6]
                elif index < 20:  # yeezus
                    source = playlists_of_albums[7]
                elif index < 23:  # tlop
                    source = playlists_of_albums[8]
                elif index < 24:  # ye
                    source = playlists_of_albums[9]
                elif index < 26:  # ksg
                    source = playlists_of_albums[10]
                elif index < 28:  # jesus is king
                    source = playlists_of_albums[11]
                elif index < 30:  # sunday service
                    source = playlists_of_albums[12]
                else:
                    return

            url = source
            destination = channel or ctx.author.voice.channel
            await destination.connect()
            server = ctx.message.guild
            voice_channel = server.voice_client
            async with ctx.typing():
                player = await YTDLSource.from_url(source, loop=client.loop)
                server_players[server.id] = player
                voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            await ctx.send(embed=now_playing_embed(player.title, url))


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


client.run('Njk2OTE2NjkyMzUzMTU1MTY0.Xovsgw.8o6EdWeLUH23MmTJE5anHv_wh4k')
