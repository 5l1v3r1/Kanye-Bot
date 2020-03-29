import asyncio
import discord
import youtube_dl


play_help_embed = discord.Embed(title="Play Help", description=".")
play_help_embed.add_field(name="song", value="!ye play Saint Pablo", inline=False)
play_help_embed.add_field(name="album", value="!ye play Graduation", inline=False)
play_help_embed.add_field(name="url", value="!ye play https://www.youtube.com/watch?v=x-FkJ5FzWgs", inline=False)
play_help_embed.add_field(name="url", value="!ye play https://www.youtube.com/watch?v=x-FkJ5FzWgs", inline=False)
play_help_embed.add_field(name="url", value="!ye play https://www.youtube.com/watch?v=x-FkJ5FzWgs", inline=False)


def now_playing_embed(title, url):
    now_playing_embed = discord.Embed(title=f"Now playing: {title}")
    return now_playing_embed


def search_for_song(search_url):
    url = ""
    return url


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
