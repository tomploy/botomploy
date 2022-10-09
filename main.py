import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

from emojis import EMOJI_NUM, EMOJI_UTIL

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
serverId = os.getenv("SERVER_ID")
clientId = os.getenv("CLIENT_ID")

intents = discord.Intents.all()

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print("Botomploy is up")

@client.command(name="ping")
async def ping(ctx):
    await ctx.channel.send("pong")

@client.command(name="vjam")
async def sondate(ctx, *props):
    content = ""
    for i in range(len(props)):
        content += EMOJI_NUM[i] + " " + props[i] + "\n"

    content += EMOJI_UTIL.get("crossmark") + " je suis nul et je peux pas venir"
    embed = discord.Embed(
        title="Sondage pour VJam!!!",
        color=discord.Color.green(),
        description=content
    )
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
    sondage = await ctx.send(embed=embed)
    for i in range(len(props)):
        await sondage.add_reaction(EMOJI_NUM[i])

    await sondage.add_reaction(EMOJI_UTIL.get("crossmark"))

client.run(token)
