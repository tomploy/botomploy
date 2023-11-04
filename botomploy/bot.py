import discord
from discord.ext import commands

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
            "commands.poll.poll",
        ]

    async def setup_hook(self):
        """
        A coroutine that syncs slash commands for the bot.
        """
        await self.tree.sync(guild=discord.Object(self.server_id))
        print(f"Synced slash commands for {self.user}.")


        for ext in self.initial_extensions:
            await self.load_extension(ext)
    
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
        await ctx.reply(error, ephemeral = True)
