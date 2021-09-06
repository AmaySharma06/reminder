from discord.ext import commands
import os
import discord
from keep_alive import keep_alive

token = os.environ.get("token")
client = commands.Bot(command_prefix=commands.when_mentioned_or("!b "),help_command=None,intents=discord.Intents.default())

extensions = [file[:-3] for file in os.listdir("./cogs") if file.endswith(".py") and file not in ("helper.py","mongo.py")]

for extension in extensions:
    client.load_extension("cogs."+extension)

print("Starting Up...")
keep_alive()
client.run(token)
