import discord
import asyncio
import configparser
from discord import FFmpegPCMAudio
from discord.ext import commands
from server import voice_blacklisted
config = configparser.ConfigParser()
config.read("files/config.ini")
voice_channel_id = config["CHANNELIDS"]["VOICE"]

class voiceCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def atthis(self, nes):
        author = nes.message.author
        id = str(nes.message.author.id)

        if voice_channel_id == str(nes.message.channel.id):
            if id in voice_blacklisted:
                await nes.send(f"Sorry, you have been blacklisted.")
                return

            elif nes.voice_client is None:
                if nes.author.voice:
                    voice = await author.voice.channel.connect()
                    voice.play(discord.FFmpegPCMAudio("files/atthis.mp3"))
                    counter = 0
                    duration = 4
                    while not counter >= duration:
                        await asyncio.sleep(1)
                        counter = counter + 1
                    await voice.disconnect()

            else:
                await nes.send(f"You are not in a voice channel!")

        else:
            await nes.send(f"Someone is already using a voice command!")

    @commands.command()
    async def die(self, nes):
        author = nes.message.author
        id = str(nes.message.author.id)

        if voice_channel_id == str(nes.message.channel.id):
            if id in voice_blacklisted:
                await nes.send(f"Sorry, you have been blacklisted.")
                return

            elif nes.voice_client is None:
                if nes.author.voice:
                    voice = await author.voice.channel.connect()
                    voice.play(discord.FFmpegPCMAudio("files/die.mp3"))
                    counter = 0
                    duration = 1
                    while not counter >= duration:
                        await asyncio.sleep(1)
                        counter = counter + 1
                    await voice.disconnect()

            else:
                await nes.send(f"You are not in a voice channel!")

        else:
            await nes.send(f"Someone is already using a voice command!")

    @commands.command()
    async def oof(self, nes):
        author = nes.message.author
        id = str(nes.message.author.id)

        if voice_channel_id == str(nes.message.channel.id):
            if id in voice_blacklisted:
                await nes.send(f"Sorry, you have been blacklisted.")
                return

            elif nes.voice_client is None:
                if nes.author.voice:
                    voice = await author.voice.channel.connect()
                    voice.play(discord.FFmpegPCMAudio("files/oof.mp3"))
                    counter = 0
                    duration = 1
                    while not counter >= duration:
                        await asyncio.sleep(1)
                        counter = counter + 1
                    await voice.disconnect()

            else:
                await nes.send(f"You are not in a voice channel!")

        else:
            await nes.send(f"Someone is already using a voice command!")

    @commands.command()
    async def wwtt(self, nes):
        author = nes.message.author
        id = str(nes.message.author.id)

        if voice_channel_id == str(nes.message.channel.id):
            if id in voice_blacklisted:
                await nes.send(f"Sorry, you have been blacklisted.")
                return

            elif nes.voice_client is None:
                if nes.author.voice:
                    voice = await author.voice.channel.connect()
                    voice.play(discord.FFmpegPCMAudio("files/wwtt.mp3"))
                    counter = 0
                    duration = 1.3
                    while not counter >= duration:
                        await asyncio.sleep(1)
                        counter = counter + 1
                    await voice.disconnect()

            else:
                await nes.send(f"You are not in a voice channel!")

        else:
            await nes.send(f"Someone is already using a voice command!")

def setup(client):
    client.add_cog(voiceCog(client))