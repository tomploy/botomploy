import os
import sys
from dotenv import load_dotenv

import discord
from discord import OptionChoice, PartialEmoji, option, Option
from discord.ext import commands

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from utils.emojis import emojis_db

load_dotenv()
class Poll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.polls = []
        super().__init__()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if(self.bot.user.id == payload.user_id):
            return
        
        guild = self.bot.get_guild(payload.guild_id);
        channel = guild.get_channel(payload.channel_id);
        msg = channel.get_partial_message(payload.message_id)

        poll = next(poll for poll in self.polls if poll.message.id == payload.message_id)

        poll.add_member(payload.emoji, payload.user_id)
        await msg.edit(embed=poll.embed)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if(self.bot.user.id == payload.user_id):
            return

        guild = self.bot.get_guild(payload.guild_id);
        channel = guild.get_channel(payload.channel_id);
        msg = channel.get_partial_message(payload.message_id)

        poll = next(poll for poll in self.polls if poll.message.id == payload.message_id)
        poll.remove_member(payload.emoji, payload.user_id)

        await msg.edit(embed=poll.embed)

    @commands.slash_command(guild_ids=[os.getenv("SERVER_ID")])
    @option("title", description="Titre du sondage")
    @option("items", description='items du sondage (virgule en separateur)')
    @option("desc", description="description du sondage", default="")
    async def poll(self, ctx: discord.ApplicationContext, 
        title: str, 
        items: str, 
        desc: str, 
        emojis: Option(str, "emojis", choices=[
            OptionChoice(name="1️⃣ Nombres", value="numbers"),
            OptionChoice(name="❤️ Coeurs", value="hearts"),
            OptionChoice(name="🟣 Ronds", value="circles"),
        ], default="circles")):

        poll = PollData(
            title,
            items.split(','),
            emojis,
            desc
        )

        self.polls.append(poll)

        sondage = await ctx.response.send_message(embed=poll.embed)
        message = await sondage.original_response()
        await poll.add_reactions(message)


empty_choice = "n o b o d y"
class PollData():
    def __init__(self, title, items, emojis, desc = ""):
        self.message = None;
        self.choices = []
        self.embed = discord.Embed(
            title=title,
            color=discord.Color.green(),
            description=desc
        )
        self.emojis = emojis_db[emojis]

        for i in range(len(items)):
            item_dict = {
                "item": items[i],
                "members": []
            }
            self.choices.append(item_dict)
            self.embed.add_field(name=str(self.emojis[i]) + " " + self.choices[i]["item"], value=empty_choice, inline=True)

    async def add_reactions(self, message):
        self.message = message
        for i in range(len(self.choices)):
            await self.message.add_reaction(self.emojis[i])
    
    def add_member(self, emoji, member):
        index = self.emojis.index(emoji)
        field = self.embed.fields[index]
        self.choices[index]["members"].append(member)

        value = ""
        for member in self.choices[index]["members"]:
            value += f"<@!{member}>\n"
            # value += ">>> <@!{}>\n".format(member)
        field.value = value;

    def remove_member(self, emoji, member):
        index = self.emojis.index(emoji)
        field = self.embed.fields[index]
        self.choices[index]["members"].remove(member)

        value = ""
        for member in self.choices[index]["members"]:
            value += f"<@!{member}>\n"

        field.value = value if len(self.choices[index]["members"]) > 0 else empty_choice;
        

def setup(bot):
    bot.add_cog(Poll(bot))
