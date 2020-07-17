 
import configparser
import discord
import os
import random
import math
from discord.ext import commands
from corpus import corpus

# Had to do this because ToS of Discord.
blacklisted_words = ["nigger", "nigga"]

funni_words = ["gay", "weeb", "weeabo", "stupid", "idiot", "moron", "nullptr"]

if os.path.isfile("files/config.ini"):
    config = configparser.ConfigParser()
    config.read("files/config.ini")
    shitpost_channel_id = int(config["CHANNEL_IDS"]["SHITPOST"])
    commands_channel_id = int(config["CHANNEL_IDS"]["COMMANDS"])
    troll_emote = config["EMOTE_ID"]["TROLL"]

else:
    print("config.ini either deleted or corrupted! Please check and try again.")
    sys.exit(0)

if os.path.isfile("files/boris_quotes.txt"):
    with open("files/boris_quotes.txt") as b_quotes:
        b_quoteData = b_quotes.readlines()

else:
    print("boris_quotes.txt either deleted or corrupted! Please check and try again.")
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
        author = nes.message.author
        await nes.send(f"{author.mention} Hello World!")

    @commands.command()
    async def quote(self, nes):
        global quoteData
        if(len(quoteData) == 0):
            with open("files/quotes.txt") as quotes:
                quoteData = quotes.readlines()

        quotes = random.choice(quoteData)
        await nes.send(f"{quotes}")
        quoteData.remove(quotes)

    @commands.command()
    async def boris(self, nes):
        global b_quoteData
        if(len(b_quoteData) == 0):
            with open("files/boris_quotes.txt") as quotes:
                b_quoteData = quotes.readlines()
    
        boris = random.choice(b_quoteData)
        await nes.send(f"{boris}")
        b_quoteData.remove(boris)

    @commands.command(aliases = ["dadjokes", "dj"])
    async def dad_jokes(self, nes):
        global jokeData
        if(len(jokeData) == 0):
            with open("files/daad_jokes.txt") as quotes:
                jokeData = quotes.readlines()

        jokes = random.choice(jokeData)
        await nes.send(f"{jokes}<:emoji_name:{troll_emote}>")
        jokeData.remove(jokes)

    @commands.command()
    async def god(self, nes, num: int):
        if(num < 1 or num > 100):
            await nes.send("The limit is 1 to 100 chars!")
        
        godsong = ""
        for i in range(0, num):
            index = math.floor(random.uniform(0, 1) * len(corpus))
            godsong = godsong + " " + corpus[index]

        await nes.send(f"{godsong}")

    @commands.command()
    async def say(self, nes, *, string: str = None):
        rand_num = 1
        string = string.replace("@", "@\u200B")
        res = string.split()
        
        for words in res:
            if words in blacklisted_words:
                await nes.message.delete()
                message = await nes.send(f"No, don't.", delete_after = 3)
                return
        
            elif "am" in res and words in funni_words:
                rand_num = random.randint(0,3)

        if(rand_num == 1):
            await nes.send(f"{string}")

        else:
            await nes.send(f"We know.")


def contains_word(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')

def setup(client):
    client.add_cog(funCog(client))
