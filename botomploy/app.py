import os
import discord
from discord.ext import commands
from botomploy.bot import Bot

""" set data path """
data_path = os.path.join(os.path.dirname(__file__), 'data') 

""" load environment variables """
token = os.getenv("DISCORD_TOKEN")
server_id = os.getenv("SERVER_ID")
client_id = os.getenv("CLIENT_ID")

def run():
    """  set discord intents """
    intents = discord.Intents.all()
    intents.message_content = True

    """ create bot """
    botomploy = Bot(client_id, server_id, intents=intents)
    """ run bot """
    botomploy.run(token)