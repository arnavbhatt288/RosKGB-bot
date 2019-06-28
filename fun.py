import configparser
import discord
import os
import random
from discord.ext import commands

config = configparser.ConfigParser()
config.read("files/config.ini")
quote_channel_id = config["CHANNELIDS"]["QUOTE"]
politics_channel_id = config["CHANNELIDS"]["POLITICS"]

with open("files/quotes.txt") as quotes:
    quoteData = quotes.readlines()

class funCog(commands.Cog):
    def __init__(self, client):
        self.client = client
	
    @commands.command()
    async def hi(self, nes):
        author = nes.message.author.mention
        await nes.send("{} Hello World!" .format(author))

    @commands.command()
    async def quote(self, nes):
        if quote_channel_id == str(nes.message.channel.id):
            quotes = random.choice(quoteData)
            await nes.send("{}" .format(quotes))

    @commands.command()
    async def pride(self, nes):
        if politics_channel_id == str(nes.message.channel.id):
            await nes.send("https://cbsnews1.cbsistatic.com/hub/i/r/2019/06/05/bcb908e0-0654-4758-a81a-f28f86182732/thumbnail/620x375/81cb5630833cdbd5c374a77feab99d77/flag-1024x619.jpg")


def setup(client):
    client.add_cog(funCog(client))