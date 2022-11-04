import os
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
from config import settings
import logging

logging.basicConfig(level=logging.WARNING)

load_dotenv()

token = os.getenv("token")

intents = nextcord.Intents.default()
intents.members = False
intents.presences = True
intents.messages = True
intents.message_content = True

client = commands.Bot(
    command_prefix=settings["PREFIX"],
    case_insensitive=True,
    intents=intents,
    activity=nextcord.Game(name=f"You cute! /help")
)

# test

# REWRITE all database to one connect at bot init and working with cursors

# ADD recursive method of cogs loading

if __name__ == "__main__":
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[: -3]}")
            print(f"cogs.{filename[: -3]} loaded")
    client.run(token, reconnect=True)
