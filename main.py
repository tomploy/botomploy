import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
serverId = os.getenv("SERVER_ID")
clientId = os.getenv("CLIENT_ID")


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    async def setup_hook(self):
        await self.tree.sync(guild=discord.Object(serverId))
        print(f"Synced slash commands for {self.user}.")
    
        
    
    async def on_ready(self):
        print("Botomploy is up")

    async def on_command_error(self, ctx, error):
        await ctx.reply(error, ephemeral = True)


intents = discord.Intents.all()
intents.message_content = True
bot = Bot(intents=intents)
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(token)

# async def main():
    
#     async with Bot(command_prefix="!", intents=intents) as bot:
#         print(token)
#         for filename in os.listdir("./cogs"):
#             if filename.endswith(".py"):
#                 await bot.load_extension(f"cogs.{filename[:-3]}")
#         await bot.start(os.getenv("DISCORD_TOKEN"))

# asyncio.run(main())

# for item in listdir(join(split(realpath(__file__))[0], "cogs")):
#     bot.load_extension("cogs." + splitext(item)[0])

# bot.run(token)