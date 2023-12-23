import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
""" load environment variables """
token = os.getenv("DISCORD_TOKEN")
server_id = os.getenv("SERVER_ID")
client_id = os.getenv("CLIENT_ID")


class Bot(commands.Bot):
    """
    A custom Discord bot that extends the commands.Bot class.

    Attributes:
    -----------
    client_id : int
        The ID of the Discord client.
    server_id : int
        The ID of the Discord server.
    """

    def __init__(self, client_id, server_id, *args, **kwargs):
        super().__init__(command_prefix = "!", *args, **kwargs)
        self.client_id = client_id
        self.server_id = server_id
        self.initial_extensions = [
            "botomploy.commands.poll",
        ]
        for ext in self.initial_extensions:
            self.load_extension(ext)
            print(f"Loaded {ext}.")
        
    async def on_ready(self):
        """
        A coroutine that runs when the bot is ready.
        """
        print("Botomploy is up")

    async def on_command_error(self, ctx, error):
        """
        A coroutine that runs when a command raises an error.

        Parameters:
        -----------
        ctx : discord.ext.commands.Context
            The context of the command.
        error : Exception
            The error raised by the command.
        """
        await ctx.reply(error)



def run():
    """  set discord intents """ 
    intents = discord.Intents.all()
    intents.message_content = True

    """ create bot """
    botomploy = Bot(client_id, server_id, intents=intents)
    """ run bot """
    botomploy.run(token)
