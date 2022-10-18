import os
from pydoc import describe
import sys
from unicodedata import name
from dotenv import load_dotenv

import discord
from discord import OptionChoice, option, Option
from discord.ext import commands

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from utils.emojis import numbers_emojis, hearts_emojis, circles_emojis

load_dotenv()


class Poll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.embed = ""
        self.emoji_arr = []
        super().__init__()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if(self.bot.user.id == payload.user_id):
            return
        guild = self.bot.get_guild(payload.guild_id);
        member = guild.get_member(payload.user_id);
        channel = guild.get_channel(payload.channel_id);
        msg = channel.get_partial_message(payload.message_id)


        field = self.embed.fields[self.emoji_arr.index(payload.emoji)]
        if(field.value == "Personne"):
            field.value = payload.member.name
        else:
            field.value += "\n" + payload.member.name
        
        await msg.edit(embeds=[self.embed])

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if(self.bot.user.id == payload.user_id):
            return
        guild = self.bot.get_guild(payload.guild_id);
        member = guild.get_member(payload.user_id);
        channel = guild.get_channel(payload.channel_id);
        msg = channel.get_partial_message(payload.message_id)

        field = self.embed.fields[self.emoji_arr.index(payload.emoji)]
        start = field.value.find(member.name)
        stop = start + len(member.name)
        if len(field.value) > stop :
            field.value = field.value[0: start:] + field.value[stop + 1::]

        await msg.edit(embeds=[self.embed])

    @commands.slash_command(guild_ids=[os.getenv("SERVER_ID")])
    @option("title", description="Titre du sondage")
    @option("items", description='items du sondage (virgule en separateur)')
    @option("desc", description="description du sondage", default="")
    async def poll(self, ctx: discord.ApplicationContext, title: str, items: str, desc: str, bullet: Option(str, "test", choices=[
            OptionChoice(name="1️⃣ Nombres", value="numbers"),
            OptionChoice(name="❤️ Coeurs", value="hearts"),
            OptionChoice(name="🟣 Ronds", value="circles"),
        ], default="circles")):

        if bullet == "numbers":
            self.emoji_arr = numbers_emojis;
        elif bullet == "hearts":
            self.emoji_arr = hearts_emojis;
        elif bullet == "circles":
            self.emoji_arr = circles_emojis;

        items_arr = items.split(',')

        embed = discord.Embed(
            title=title,
            color=discord.Color.green(),
            description=desc
        )

        for i in range(len(items_arr)):
            embed.add_field(name=str(self.emoji_arr[i]) + " " + items_arr[i], value="Personne", inline=True)
            # content +=  + "\n"

        # embed.add_field(name=EMOJI_UTIL.get("crossmark") + " Indispo", value="Personne", inline=True)
        # content += 

        self.embed = embed

        sondage = await ctx.response.send_message(embeds=[embed])


        message = await sondage.original_response();

        for i in range(len(items_arr)):
            await message.add_reaction(self.emoji_arr[i])

        # await message.add_reaction(EMOJI_UTIL.get("crossmark"))
        # await wait_for_reactions(ctx, sondage, client, props)


def setup(bot):
    bot.add_cog(Poll(bot))
