import discord
from pymongo import MongoClient
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URL"), int(os.getenv("MONGO_PORT")))
db = client.get_database("GuildData").get_collection("GuildConfig")


def determine_prefix(bot, message):
    try:
        guild = message.guild
        prefix = db.find({"guildID": guild.id})
        return prefix[0]['prefix']
    except AttributeError:
        return os.getenv("PREFIX")


class BayBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self._cogs = ['cogs.music', 'cogs.example']
        super().__init__(command_prefix=determine_prefix, case_insensitive=True)

    async def on_connect(self):
        print(f"""[ BOT ] Connected to Discord (latency: {self.latency*1000:,.0f} ms).""")

    async def on_ready(self):
        SlashCommand(self, sync_commands=True)
        print("[ BOT ] Running setup...")
        for cog in self._cogs:
            self.load_extension(cog)
            print(f"[ BOT | Load ] Loaded `{cog}` cog.")
        print("[ BOT ] Setup complete.")
        print("[ BOT ] Logged in")

    async def on_guild_join(self, guild):
        dictionary = {
                "guildID": guild.id,
                "prefix": os.getenv("PREFIX"),
                "welcomeChannelId": None,
                "goodbyeChannelId": None
            }
        x = db.insert_one(dictionary)
        del x


intents = discord.Intents.all()
bot = BayBot(intents=intents)
bot.run(os.getenv("TOKEN"))
