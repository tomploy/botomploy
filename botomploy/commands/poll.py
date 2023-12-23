import os
import discord
from discord.ext import commands
from botomploy.commands.pollData import PollData
import botomploy.settings as settings

import jsonpickle

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.polls = []
        print("loading polls")
        """ load polls """
        with open(settings.data_path + "/poll.json", "r") as infile:
            jsonpoll = infile.read()
            self.polls = jsonpickle.decode(jsonpoll)

        super().__init__()

    def get_message(self, channel, messaged_id):
        """ retrieve a message from a channel """
        guild = self.bot.get_guild(self.bot.server_id)
        channel = guild.get_channel(channel)
        return channel.get_partial_message(messaged_id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if(self.bot.user.id == payload.user_id):
            return

        msg = self.get_message(payload.channel_id, payload.message_id)

        poll = next(poll for poll in self.polls if poll.message.id == payload.message_id)

        poll.add_member(payload.emoji, payload.user_id)
        await msg.edit(embed=poll.embed)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if(self.bot.user.id == payload.user_id):
            return

        msg = self.get_message(payload.channel_id, payload.message_id)

        poll = next(poll for poll in self.polls if poll.message.id == payload.message_id)
        poll.remove_member(payload.emoji, payload.user_id)

        await msg.edit(embed=poll.embed)

    @commands.slash_command(guild_ids=[os.getenv("SERVER_ID")])
    @discord.option("title", description="Titre du sondage")
    @discord.option("desc", description="description du sondage")
    @discord.option("items", description='items du sondage (virgule en separateur)')
    async def poll(self, ctx: discord.ApplicationContext, 
        title: str, 
        desc: str, 
        items: str, 
        emojis: discord.Option(str, "emojis", choices=[
            discord.OptionChoice(name="1️⃣ Nombres", value="numbers"),
            discord.OptionChoice(name="❤️ Coeurs", value="hearts"),
            discord.OptionChoice(name="🟣 Ronds", value="circles"),
        ], default="circles")):

        poll = PollData(title, items.split(','), emojis, desc)
        sondage = await ctx.response.send_message(embed=poll.embed)
        message = await sondage.original_response()
        poll.message = message
        self.polls.append(poll)

        jsonpoll = jsonpickle.encode(self.polls)
        with open("poll.json", "w") as outfile:
            outfile.write(jsonpoll)

        await poll.add_reactions(message)

    async def cog_load(self):
        """ load polls """
        with open("poll.json", "r") as infile:
            jsonpoll = infile.read()
            self.polls = jsonpickle.decode(jsonpoll)

def setup(bot):
    bot.add_cog(Poll(bot))
