import discord
import sys

client = discord.Client()

@client.event
async def on_ready():
    print("The bot is ready!")
    await client.change_presence(activity=discord.Game(name='Spamming @everyone'))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "invoke black":
        while True:
            await message.channel.send(":regional_indicator_n: :regional_indicator_i: :regional_indicator_i: :regional_indicator_g: :regional_indicator_e: :regional_indicator_r:")
    if message.content == "stop":
        await client.close()
        sys.exit()


client.run('NjkyNTc2MTcxOTAwMTQxNTk4.Xnwk-w.3uBGgDEIGKfilvdotEJwOnH-eIw')