import os
import discord
from discord.ext import commands
from botomploy.commands.pollData import PollData
from botomploy.utils.emojis import emojis

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
        guild = self.bot.get_guild(int(self.bot.server_id))
        channel = guild.get_channel(channel)
        return channel.get_partial_message(messaged_id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if(self.bot.user.id == payload.user_id):
            return

        msg = self.get_message(payload.channel_id, payload.message_id)

        print(payload.message_id)
        print(type(payload.message_id))
        for poll in self.polls:
            print(poll)
            print(type(poll))
        poll = self.polls[str(payload.message_id)]

        poll.add_member(payload.emoji, payload.user_id)

        await msg.edit(embed=poll.embed())

        self.save_polls()

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if(self.bot.user.id == payload.user_id):
            return

        msg = self.get_message(payload.channel_id, payload.message_id)

        print(payload.message_id)
        print(type(payload.message_id))
        for poll in self.polls:
            print(poll)
            print(type(poll))
        poll = self.polls[str(payload.message_id)]

        poll.remove_member(payload.emoji, payload.user_id)

        await msg.edit(embed=poll.embed())

        self.save_polls()

    @commands.slash_command(guild_ids=[os.getenv("SERVER_ID")], description="Créer un sondage (9 max)")
    @discord.option("title", description="Titre du sondage")
    @discord.option("desc", description="description du sondage")
    @discord.option("items", description='items du sondage (virgule en separateur)')
    async def poll(self, ctx: discord.ApplicationContext, 
        title: str, 
        desc: str, 
        items: str, 
        emoji_type: discord.Option(str, "emojis", choices=[
            discord.OptionChoice(name="1️⃣ Nombres", value="numbers"),
            discord.OptionChoice(name="❤️ Coeurs", value="hearts"),
            # discord.OptionChoice(name="🟣 Ronds", value="circles"),
        ], default="circles")):

        poll = PollData(title, items.split(','), emoji_type, desc)
        sondage = await ctx.response.send_message(embed=poll.embed())
        message = await sondage.original_response()
        poll.message_id = message.id
        self.polls[poll.message_id] = poll
        self.save_polls()

        for i in range(len(poll.choices)):
            await message.add_reaction(emojis[poll.emoji_type][i])

    def save_polls(self):
        jsonpoll = jsonpickle.encode(self.polls)
        with open(settings.data_path + "/poll.json", "w") as outfile:
            outfile.write(jsonpoll)

def setup(bot):
    bot.add_cog(Poll(bot))
