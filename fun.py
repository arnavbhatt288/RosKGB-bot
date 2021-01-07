
import configparser
import discord
import os
import random
import math
from discord.ext import commands
from discord.utils import get
from corpus import corpus

# Had to do this because ToS of Discord.
blacklisted_words = ["nigger", "nigga"]

if os.path.isfile("files/config.ini"):
    config = configparser.ConfigParser()
    config.read("files/config.ini")
    admin_role = config["ROLE_NAMES"]["ADMINISTRATOR"]
    mod_role = config["ROLE_NAMES"]["MODERATOR"]
    shitpost_channel_id = config["CHANNEL_IDS"]["SHITPOST"]
    commands_channel_id = config["CHANNEL_IDS"]["COMMANDS"]
    troll_emote = config["EMOTE_ID"]["TROLL"]

else:
    print("config.ini either deleted or corrupted! Please check and try again.")
    sys.exit(0)

if os.path.isfile("files/quotes.txt"):
    with open("files/quotes.txt") as quotes:
        quoteData = quotes.readlines()

else:
    print("quotes.txt either deleted or corrupted! Please check and try again.")
    sys.exit(0)


if os.path.isfile("files/dad_jokes.txt"):
    with open("files/dad_jokes.txt") as jokes:
        jokeData = jokes.readlines()

else:
    print("dad_jokes.txt either deleted or corrupted! Please check and try again.")

class funCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hi(self, nes):
        if(channel_check(nes) == False):
            return

        author = nes.message.author
        await nes.send(f"{author.mention} Hello World!")

    @commands.command()
    async def quote(self, nes):
        if(channel_check(nes) == False):
            return

        global quoteData
        if(len(quoteData) == 0):
            with open("files/quotes.txt") as quotes:
                quoteData = quotes.readlines()

        quotes = random.choice(quoteData)
        await nes.send(quotes)
        quoteData.remove(quotes)

    @commands.command(aliases = ["dadjokes", "dj"])
    async def dad_jokes(self, nes):
        if(channel_check(nes) == False):
            return

        global jokeData
        if(len(jokeData) == 0):
            with open("files/dad_jokes.txt") as quotes:
                jokeData = quotes.readlines()

        jokes = random.choice(jokeData)
        await nes.send(f"{jokes}<:emoji_name:{troll_emote}>")
        jokeData.remove(jokes)

    @commands.command()
    async def god(self, nes, *, string: str = None):
        if(channel_check(nes) == False):
            return

        num = len(string.split())
        if(num < 1 or num > 100):
            await nes.send("The limit is 1 to 100 chars!")
            return

        godsong = ""
        for i in range(0, num):
            index = math.floor(random.uniform(0, 1) * len(corpus))
            godsong = godsong + " " + corpus[index]

        await nes.send(godsong)

    @commands.command()
    async def say(self, nes, *, string: str = None):
        if(channel_check(nes) == False):
            return

        string = string.replace("@", "@\u200B")

        res = string.split()
        for words in res:
            if words in blacklisted_words:
                await nes.message.delete()
                message = await nes.send(f"No, don't.", delete_after = 3)
                return

        await nes.send(string)

    @god.error
    async def god_error(self, nes, error):
        error = getattr(error, "original", error)
        if isinstance(error, commands.BadArgument):
            await nes.send("Enter the argument as string!")

def channel_check(nes):
    channel_id = str(nes.message.channel.id)

    if(channel_id == shitpost_channel_id or channel_id == commands_channel_id):
        return True

    else:
        role = get(nes.guild.roles, name = admin_role)
        if role in nes.author.roles:
            return True

        role = get(nes.guild.roles, name = mod_role)
        if role in nes.author.roles:
            return True

        return False

def setup(client):
    client.add_cog(funCog(client))
