import os
from os import listdir
from os.path import realpath, split, join, splitext
from dotenv import load_dotenv
import discord
from discord.ext import commands


load_dotenv()
token = os.getenv("DISCORD_TOKEN")
serverId = os.getenv("SERVER_ID")
clientId = os.getenv("CLIENT_ID")


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix="!", 
            intents=intents)
        

    # async def setup_hook(self):
        # await self.tree.sync(guild=discord.Object(serverId))
        # print(f"Synced slash commands for {self.user}.");
    
    async def on_ready(self):
        print("Botomploy is up")

    async def on_command_error(self, ctx, error):
        await ctx.reply(error, ephemeral = True)

bot = Bot()

for item in listdir(join(split(realpath(__file__))[0], "cogs")):
    bot.load_extension("cogs." + splitext(item)[0])

bot.run(token)