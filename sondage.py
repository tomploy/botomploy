import discord
from asyncio import sleep
from discord.ext import commands

from emojis import EMOJI_NUM, EMOJI_UTIL

async def wait_for_reactions(ctx, msg, client, props):
    await sleep(86400) # 24 heures
    cached_msg = discord.utils.get(client.cached_messages, id=msg.id)
    react_l = []
    for i in range(len(cached_msg.reactions)-1):
        if (str(cached_msg.reactions[i]) == EMOJI_NUM[i]):
            react_l.append((props[i], cached_msg.reactions[i].count-1))
    react_l.append(("on est des nullos on annule", cached_msg.reactions[len(cached_msg.reactions)-1].count-1))
    
    content = ""
    for react in react_l:
        content += str(react[0]) + " : " + str(react[1]) + "\n"
    embed = discord.Embed(
        title="Résultaaats",
        color=discord.Color.green(),
        description=content
    )
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

    await ctx.send(embed=embed)
