import os
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
from config import settings

load_dotenv()

token = os.getenv("token")

client = commands.Bot(
    command_prefix=settings["PREFIX"],
    case_insensitive=True,
    intents=nextcord.Intents.all(),
)


if __name__ == "__main__":
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[: -3]}")
            print(f"cogs.{filename[: -3]} loaded")
    client.run(token, reconnect=True)
