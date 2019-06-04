
import configparser
import datetime
import discord
import logging
import pickle
import random
import signal
import sys
import time
import os
from bugcheck import bugdict
from discord.ext import commands
from discord.utils import get
from mmresult import mmdict
from ntstatus import ntdict
from hresult import hrdict
from winerror import windict
from wm import wmdict
client = commands.Bot(command_prefix = "$")
client.remove_command("help")

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

# Loading necessary files
if os.path.isfile("files/config.ini"):
    config = configparser.ConfigParser()
    config.read("files/config.ini")
    token = config["CREDENTIALS"]["TOKEN"]
    server_owner_id = config["CREDENTIALS"]["SERVEROWNERID"]

else:
    print("config.ini either deleted or corrupted! Please check and try again.")
    sys.exit(0)

if os.path.isfile("files/blacklist.dat"):
    try:
        with open("files/blacklist.dat", "rb") as blacklist:
            blacklisted = pickle.load(blacklist)

    except EOFError:
        blacklisted = []

else:
    print("blacklist.dat is either deleted or corrupted! Please check and try again.")

if os.path.isfile("files/quotes.txt"):
    with open("files/quotes.txt") as quotes:
        quoteData = quotes.readlines()

else:
    print("quotes.txt is either deleted or corrupted! Please check and try again.")
# Start of the bot

@client.event
async def on_ready():
    print("Bot is online as {0.user}" .format(client))

@client.event
async def on_message(message):
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d %H:%M")
    file = open("chat.txt", "a")

    file.write(str(today) + f" {message.channel}: {message.author}: {message.content}\n")
    file.close()
    
    await client.process_commands(message)

# Error code commands

@client.command(pass_context = True)
async def bugcheck(nes, value: str):
    if any(c in value for c in "x"):
        value = value[2:]

    if len(value) < 8:
        strValue = 8 - len(value)
        value = "0" * strValue + value

    if value in bugdict:
        await nes.send("The meaning of this error code is - `{}`" .format(bugdict[value]))

    else:
        await nes.send(f"Error code not found! Please check the code and try again.")

@client.command(pass_context = True)
async def hresult(nes, value: str):
    if any(c in value for c in "x"):
        value = value[2:]

    if len(value) < 8:
        strValue = 8 - len(value)
        value = "0" * strValue + value

    if value in hrdict:
        await nes.send("The meaning of this error code is - `{}`" .format(hrdict[value]))

    else:
        await nes.send(f"Error code not found! Please check the code and try again.")

@client.command(pass_context = True)
async def mmresult(nes, value: str):
    if any(c in value for c in "x"):
        value = value[2:]

    if len(value) < 8:
        strValue = 8 - len(value)
        value = "0" * strValue + value

    if value in mmdict:
        await nes.send("The meaning of this error code is - `{}`" .format(mmdict[value]))

    else:
        await nes.send(f"Error code not found! Please check the code and try again.")

@client.command(pass_context = True)
async def ntstatus(nes, value: str):
    if any(c in value for c in "x"):
        value = value[2:]

    if len(value) < 8:
        strValue = 8 - len(value)
        value = "0" * strValue + value

    if value in ntdict:
        await nes.send("The meaning of this error code is - `{}`" .format(ntdict[value]))

    else:
        await nes.send(f"Error code not found! Please check the code and try again.")

@client.command(pass_context = True)
async def winerror(nes, value: str):
    if any(c in value for c in "x"):
        value = value[2:]

    if len(value) < 8:
        strValue = 8 - len(value)
        value = "0" * strValue + value

    if value in windict:
        await nes.send("The meaning of this error code is - `{}`" .format(windict[value]))

    else:
        await nes.send(f"Error code not found! Please check the code and try again.")

@client.command(pass_context = True)
async def wm(nes, value: str):
    if any(c in value for c in "x"):
        value = value[2:]

    if len(value) < 8:
        strValue = 8 - len(value)
        value = "0" * strValue + value

    if value in wmdict:
        await nes.send("The meaning of this error code is - `{}`" .format(wmdict[value]))

    else:
        await nes.send(f"Error code not found! Please check the code and try again.")

# Server commands

@client.command(pass_context = True)
@commands.has_any_role("Admins", "Moderators")
async def blacklist(nes, value: str):
    if len(value) == 18 and value.isdigit():
        if value in blacklisted:
            await nes.send(f"User already exists!")

        else:
            blacklisted.append(value)
            await nes.send(f"User blacklisted.")

    else:
        await nes.send(f"Invalid User ID! Please try again.")

@client.command(pass_context = True)
async def listblacklist(nes):
    listBlacklist = str(blacklisted)[1:-1]

    if not blacklisted:
        await nes.send(f"No one is blacklisted.")

    else:
        await nes.send(f"List of User IDs blacklisted - ")
        await nes.send("`{}`" .format(listBlacklist))

@client.command(pass_context = True)
async def pol(nes):
    author = nes.message.author
    id = str(nes.message.author.id)
    role = get(author.guild.roles, name = "Politics")

    if id in blacklisted:
        await nes.send(f"Sorry, you have been blacklisted.")
        return

    elif role in author.roles:
        await nes.send(f"You already have the role!")

    else:
        await author.add_roles(role)
        await nes.send(f"Role assigned to you.")

@client.command(pass_context = True)
@commands.has_any_role("Admins", "Moderators")
async def unblacklist(nes, value: str):
    if len(value) == 18 and value.isdigit():
        if value in blacklisted:
            blacklisted.remove(value)
            await nes.send(f"User unblacklisted.")

        else:
            await nes.send(f"User doesn't exist! Please try again.")

    else:
        await nes.send(f"Invalid User ID! Please try again.")

@client.command(pass_context = True)
async def unpol(nes):
    author = nes.message.author
    id = str(nes.message.author.id)
    role = get(author.guild.roles, name = "Politics")

    if id in blacklisted:
        await nes.send(f"Sorry, you have been blacklisted.")
        return

    elif not role in author.roles:
        await nes.send(f"You already don't have the role!")

    else:
        await author.remove_roles(role)
        await nes.send(f"Role removed from you.")

# Bot commands only accessible by owner of server

def ownerShutdown(signal, frame):
    with open("files/blacklist.dat", "wb") as blacklist:
        pickle.dump(blacklisted, blacklist)

    print(f"\nShutting down...")
    time.sleep(3)
    sys.exit(0)

@client.command(pass_context = True)
async def shutdown(nes):
    if str(nes.message.author.id) == server_owner_id:
        with open("files/blacklist.dat", "wb") as blacklist:
            pickle.dump(blacklisted, blacklist)

        await nes.send(f"Shutting down...")
        time.sleep(3)
        sys.exit(0)

    else:
        return

@client.command(pass_context = True)
async def reboot(nes):
    if str(nes.message.author.id) == server_owner_id:
        with open("blacklist.dat", "wb") as blacklist:
            pickle.dump(blacklisted, blacklist)

        await nes.send(f"Rebooting...")
        time.sleep(3)
        python = sys.executable
        os.execl(python, python, *sys.argv)

    else:
        return

# Other commands

@client.command(pass_context = True)
async def about(nes):
    await nes.send("RosKGB V2.5\nCopyright 2019 Arnav Bhatt (arnavbhatt288). Proudly hosted by Cernodile.")

@client.command(pass_context = True)
async def help(nes):
    embed = discord.Embed(
        colour = discord.Colour.blue()
    )

    embed.set_author(name = "RosKGB V2.5 - Commands")
    embed.add_field(name = "$bugcheck <VALUE>", value = "Gives meaning of bugcheck codes.", inline = False)
    embed.add_field(name = "$blacklist <VALUE>", value = "(ONLY FOR ADMIN AND MODERATORS) Blacklists an user for usage of $pol and $unpol command.", inline = False)
    embed.add_field(name = "$unblacklist <VALUE>", value = "(ONLY FOR ADMIN AND MODERATORS) Unblacklists an user for usage of $pol and $unpol command.", inline = False)
    embed.add_field(name = "$hi", value = "Says hello world to you.", inline = False)
    embed.add_field(name = "$hresult <VALUE>", value = "Gives meaning of hresult codes.", inline = False)
    embed.add_field(name = "$mmresult <VALUE>", value = "Gives meaning of mmresult codes.", inline = False)
    embed.add_field(name = "$ntstatus <VALUE>", value = "Gives meaning of ntstatus codes.", inline = False)
    embed.add_field(name = "$pol", value = "Gives Politics role to you.", inline = False)
    embed.add_field(name = "$quote", value = "Gives some random quote to you.", inline = False)
    embed.add_field(name = "$unpol", value = "Removes Politics role from you.", inline = False)
    embed.add_field(name = "$winerror <VALUE>", value = "Gives meaning of Win32 error codes.", inline = False)
    embed.add_field(name = "$wm <VALUE>", value = "Gives meaning of WindowMessage codes.", inline = False)
    await nes.send(embed = embed)

@client.command(pass_context = True)
async def hi(nes):
    author = nes.message.author.mention
    await nes.send("{} Hello World!" .format(author))

@client.command(pass_context = True)
async def quote(nes):
    quotes = random.choice(quoteData)
    await nes.send("{}" .format(quotes))

# Other stuffs

signal.signal(signal.SIGINT, ownerShutdown)

client.run(token)
