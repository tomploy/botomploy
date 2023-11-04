import os
import discord
from discord.ext import commands
from botomploy import Bot
from dotenv import load_dotenv


def run():
    """ load environment variables """
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    server_id = os.getenv("SERVER_ID")
    client_id = os.getenv("CLIENT_ID")

    """  set discord intents """
    intents = discord.Intents.all()
    intents.message_content = True

    """ create bot """
    bot = Bot(client_id, server_id, intents=intents)

    """ load cogs """
    bot.load_extension("botomploy.commands.poll.poll")

    """ run bot """
    bot.run(token)