import os
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from botomploy.commands.pollData import PollData
from botomploy.utils.emojis import emojis

import botomploy.settings as settings

import jsonpickle

class Poll(commands.Cog):
    """ Poll cog """
    def __init__(self, bot):
        self.bot = bot
        self.polls = []
        print("loading polls")
        """ load polls """
        with open(settings.data_path + "/poll.json", "r") as infile:
            jsonpoll = infile.read()
            self.polls = jsonpickle.decode(jsonpoll)

        super().__init__()

    """ slash commands ========================================================================== """

    """ TODO :  ajouter une date de fin au sondage"""

    """ create a command group outside of init to be used for subcommand decorators"""
    poll = SlashCommandGroup(name="poll", description="Toutes les commandes relatives aux sondages")

    @poll.command(description="Créer un sondage (9 max)")
    @discord.option("title", description="Titre du sondage")
    @discord.option("desc", description="description du sondage")
    @discord.option("items", description='items du sondage (virgule en separateur)')
    async def new(self, ctx: discord.ApplicationContext, 
        title: str, 
        desc: str, 
        items: str, 
        emoji_type: discord.Option(str, "emojis", choices=[
            discord.OptionChoice(name="1️⃣ Nombres", value="numbers"),
            discord.OptionChoice(name="❤️ Coeurs", value="hearts"),
            # discord.OptionChoice(name="🟣 Ronds", value="circles"),
        ], default="numbers")):
        """  slash command to create a poll """

        items = items.split(',')
        if(len(items) > 9):
            await ctx.response.send_message("Trop d'items ! (9 max)")
            return

        poll = PollData(title, items, emoji_type, desc)
        sondage = await ctx.response.send_message(embed=poll.embed())
        message = await sondage.original_response()
        poll.message_id = message.id
        poll.channel_id = ctx.channel_id
        self.polls[poll.message_id] = poll
        self.save_polls()

        """ add reactions to the message sent by the bot"""
        for i in range(len(poll.choices)):
            await message.add_reaction(emojis[poll.emoji_type][i])

    @poll.command(description="Supprimer un sondage")
    @discord.option("message_id", description="ID du message du sondage")
    async def delete(self, ctx: discord.ApplicationContext, message_id: int):
        """  slash command to delete a poll """
        msg = self.get_message(ctx.channel_id, message_id)
        await msg.delete()
        del self.polls[str(message_id)]
        self.save_polls()

 
    @poll.command(description="Lister les sondages")
    async def list(self, ctx: discord.ApplicationContext):
        """  slash command to list all polls 
        TODO : ne permettre de ne l'utiliser que dans le channel du bot et renvoyer un  message ephemere si ce n'est pas le cas """
        embed = discord.Embed(
            title="Liste des sondages",
            color=discord.Color.purple(),
        )

        msg = ""
        for poll in self.polls:
            name = f"{self.polls[poll].title}\n"
            value = f"[{self.polls[poll].desc}](https://discordapp.com/channels/{self.bot.server_id}/{self.polls[poll].channel_id}/{self.polls[poll].message_id})\n"
            for i in range(len(self.polls[poll].choices)):
                value += f"{emojis[self.polls[poll].emoji_type][i]} {self.polls[poll].choices[i]['item']} ({len(self.polls[poll].choices[i]['members'])})\n"
            embed.add_field(name=name, value=value, inline=False)

            msg += f"{poll} : {self.polls[poll].title}\n"
        await ctx.response.send_message(embed=embed)


    """ TODO : faire en sorte que seulement l'auteur du sondage puisse modifier le sondage """
    @poll.command(description="Modifier un sondage")
    @discord.option("message_id", description="ID du message du sondage", default="")
    @discord.option("title", description="Titre du sondage", default="")
    @discord.option("desc", description="description du sondage", default="")
    async def edit(self, ctx: discord.ApplicationContext, message_id: int, title: str, desc: str):
        """  slash command to edit a poll """
        msg = self.get_message(ctx.channel_id, message_id)
        poll = self.polls[str(message_id)]
        poll.title = title
        poll.desc = desc
        await msg.edit(embed=poll.embed())
        self.save_polls()
                   

    """ event listeners ========================================================================== """
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """event listener for reaction add, add the member to the poll and edit the message"""
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
        """event listener for reaction remove, remove the member from the poll and edit the message"""
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

    """ utility functions ========================================================================== """
    def get_message(self, channel, messaged_id):
        """ utility function : retrieve a message from a channel """
        guild = self.bot.get_guild(int(self.bot.server_id))
        channel = guild.get_channel(channel)
        return channel.get_partial_message(messaged_id)
    
    def save_polls(self):
        jsonpoll = jsonpickle.encode(self.polls)
        with open(settings.data_path + "/poll.json", "w") as outfile:
            outfile.write(jsonpoll)


""" setup the cog  ========================================================================== """
def setup(bot):
    bot.add_cog(Poll(bot))
