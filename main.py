
import discord
import pickle
import asyncio
import configparser
import datetime
import logging
import signal
import sys
import time
import traceback
import os
from discord.ext import commands

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

extensions = ["error_code", "fun"]

bot_prefix = "--"

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = bot_prefix, intents = intents)
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = f"for {bot_prefix}help"))
    print("Bot is online as {0.user}" .format(client))

@client.event
async def on_message(message):
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d %H:%M")
    file = open("chat.txt", "a")

    file.write(str(today) + f" {message.channel}: {message.author}: {message.content}\n")
    file.close()

    await client.process_commands(message)

@client.event
async def on_member_join(member):
    author = member.mention
    server = member.guild.name
    rules_channel = client.get_channel(rules_channel_id)
    readme_channel = client.get_channel(readme_channel_id)
    instructional_channel = client.get_channel(instructional_channel_id)
    general_channel = client.get_channel(general_channel_id)

    for channel in member.guild.channels:
        if channel == general_channel:
            await channel.send(introduction .format(author, server, rules_channel.mention, readme_channel.mention, instructional_channel.mention))

@client.command(pass_context = True)
async def shutdown(nes):
    role = discord.utils.get(nes.guild.roles, name = admin_role)
    if str(nes.message.author.id) == server_owner_id or role in nes.author.roles:
        await nes.send("Shutting down...")
        time.sleep(3)
        sys.exit(0)

    else:
        await nes.send("You do not have enough permissions to shut down the bot!")
        return

@client.command(pass_context = True)
async def reboot(nes):
    role = discord.utils.get(nes.guild.roles, name = admin_role)
    if str(nes.message.author.id) == server_owner_id or role in nes.author.roles:
        await nes.send("Rebooting...")
        time.sleep(3)
        python = sys.executable
        os.execl(python, python, *sys.argv)

    else:
        await nes.send("You do not have enough permissions to restart the bot!")
        return

@client.command(pass_context = True)
async def help(nes, value: str = None):
    embed = discord.Embed(
        colour = discord.Colour.blue()
    )
    avatar = client.user.avatar_url

    if not value:
        embed.set_author(name = "RosKGB V1.2 - Help")
        embed.set_thumbnail(url = avatar)
        embed.add_field(name = f"{bot_prefix}help error_code", value = "Lists commands for the error codes.", inline = False)
        embed.add_field(name = f"{bot_prefix}help fun", value = "Lists commands for having fun.", inline = False)
        await nes.send(embed = embed)

    elif value == "error_code":
        embed.set_author(name = "RosKGB V1.2 - Help - Error Code")
        embed.set_thumbnail(url = avatar)
        embed.add_field(name = f"{bot_prefix}bc OR {bot_prefix}bugcheck <VALUE>", value = "Gives meaning of bugcheck (BSoD) STOP codes.", inline = False)
        embed.add_field(name = f"{bot_prefix}hr OR {bot_prefix}hresult <VALUE>", value = "Gives meaning of HRESULT (result of a handle) codes.", inline = False)
        embed.add_field(name = f"{bot_prefix}mm OR {bot_prefix}multimedia <VALUE>", value = "Gives meaning of MM (Multimedia API) codes.", inline = False)
       	embed.add_field(name = f"{bot_prefix}nt OR {bot_prefix}ntresult  <VALUE>", value = "Gives meaning of NT codes.", inline = False)
        embed.add_field(name = f"{bot_prefix}win32 OR {bot_prefix}winerror <VALUE>", value = "Gives meaning of Win32 codes.", inline = False)
        embed.add_field(name = f"{bot_prefix}wm OR {bot_prefix}windowmessge <VALUE>", value = "Gives meaning of WM (Window USER message) codes.", inline = False)
        await nes.send(embed = embed)

    elif value == "fun":
        embed.set_author(name = "RosKGB V1.2 - Help - Fun")
        embed.set_thumbnail(url = avatar)
        embed.add_field(name = f"{bot_prefix}dadjokes OR {bot_prefix}dj", value = f"Gives you random dad jokes!", inline = False)
        embed.add_field(name = f"{bot_prefix}god \"<string>\"", value = f"Talk with god! (Maximum words 1-100)", inline = False)
        embed.add_field(name = f"{bot_prefix}hi", value = f"Says hello to you!", inline = False)
        embed.add_field(name = f"{bot_prefix}quotes", value = f"Gives you some random quotes!", inline = False)
        embed.add_field(name = f"{bot_prefix}say \"<string>\"", value = f"Repeats every sentence you say!", inline = False)
        await nes.send(embed = embed)

    else:
        await nes.send("Invalid choice! Please try again")

if __name__ == "__main__":
    for extension in extensions:
        try:
            client.load_extension(extension)
        except(discord.ClientException, ModuleNotFoundError):
            print(f"Failed to load extension {extension}.")
            traceback.print_exc()

    if os.path.isfile("files/config.ini"):
        config = configparser.ConfigParser()
        config.read("files/config.ini")
        token = config["CREDENTIALS"]["TOKEN"]
        server_owner_id = config["CREDENTIALS"]["SERVEROWNERID"]
        general_channel_id = int(config["CHANNEL_IDS"]["GENERAL"])
        rules_channel_id = int(config["CHANNEL_IDS"]["RULES"])
        readme_channel_id = int(config["CHANNEL_IDS"]["README"])
        instructional_channel_id = int(config["CHANNEL_IDS"]["INSTRUCTIONS"])
        admin_role = config["ROLE_NAMES"]["ADMINISTRATOR"]
        introduction = config["INTRODUCTION"]["INTRODUCTION"]

    else:
        print("config.ini either deleted or corrupted! Please check and try again.")
        sys.exit(0)

    client.run(token, bot = True, reconnect = True)
