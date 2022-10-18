import os
import sys
from unicodedata import name
from dotenv import load_dotenv

import discord
from discord import option
from discord.ext import commands

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from utils.emojis import poll_number_emojis, EMOJI_UTIL

load_dotenv()


class Poll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.embed = "";
        super().__init__()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if(self.bot.user.id == payload.user_id):
            return
        guild = self.bot.get_guild(payload.guild_id);
        member = guild.get_member(payload.user_id);
        channel = guild.get_channel(payload.channel_id);
        msg = channel.get_partial_message(payload.message_id)


        field = self.embed.fields[poll_number_emojis.index(payload.emoji)]
        if(field.value == "Personne"):
            field.value = member.name
        else:
            field.value += "\n" + member.name
        
        await msg.edit(embeds=[self.embed])

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if(self.bot.user.id == payload.user_id):
            return
        guild = self.bot.get_guild(payload.guild_id);
        member = guild.get_member(payload.user_id);
        channel = guild.get_channel(payload.channel_id);
        msg = channel.get_partial_message(payload.message_id)

        field = self.embed.fields[poll_number_emojis.index(payload.emoji)]
        start = field.value.find(member.name)
        stop = start + len(member.name)
        if len(field.value) > stop :
            field.value = field.value[0: start:] + field.value[stop + 1::]

        await msg.edit(embeds=[self.embed])

    @commands.slash_command(guild_ids=[os.getenv("SERVER_ID")])
    @option("title", description="Titre du sondage")
    @option("items", description='items du sondage (virgule en separateur)')
    @option("desc", description="description du sondage", default="")
    async def poll(self, ctx: discord.ApplicationContext, title: str, items: str, desc: str):

        emoji_arr = poll_number_emojis;
        items_arr = items.split(',')

        embed = discord.Embed(
            title=title,
            color=discord.Color.green(),
            description=desc
        )

        for i in range(len(items_arr)):
            embed.add_field(name=str(emoji_arr[i]) + " " + items_arr[i], value="Personne", inline=True)
            # content +=  + "\n"

        # embed.add_field(name=EMOJI_UTIL.get("crossmark") + " Indispo", value="Personne", inline=True)
        # content += 

        self.embed = embed

        sondage = await ctx.response.send_message(embeds=[embed])


        message = await sondage.original_response();

        for i in range(len(items_arr)):
            await message.add_reaction(emoji_arr[i])

        # await message.add_reaction(EMOJI_UTIL.get("crossmark"))
        # await wait_for_reactions(ctx, sondage, client, props)


def setup(bot):
    bot.add_cog(Poll(bot))
