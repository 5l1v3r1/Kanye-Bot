import discord

def embed_help(list_of_list):
    total = len(list_of_list)
    embed = discord.Embed(title="Commands List", description=f"{total} Total\n", color=0xff0000)
    embed.set_author(name="Kanye Bot", icon_url="https://i.imgur.com/5TFj51C.jpg")
    embed.set_thumbnail(url="https://i.imgur.com/CyLtauV.jpg")
    for list in list_of_list:
        embed.add_field(name=list[0], value=list[1], inline=False)
    embed.set_footer(text="Thank you for using Kanye Bot! Devloped by Nman4#6604 https://github.com/NMan1")
    return embed




