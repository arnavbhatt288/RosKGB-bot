import discord
import asyncio
import configparser
import datetime
import logging
import pickle
import signal
import sys
import time
import traceback
import os
from discord.ext import commands
from server import blacklisted
client = commands.Bot(command_prefix = "$")
client.remove_command("help")

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

if os.path.isfile("files/config.ini"):
    config = configparser.ConfigParser()
    config.read("files/config.ini")
    token = config["CREDENTIALS"]["TOKEN"]
    server_owner_id = config["CREDENTIALS"]["SERVEROWNERID"]

else:
    print("config.ini either deleted or corrupted! Please check and try again.")
    sys.exit(0)

extensions = ["fun", "server", "error_code"]


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

def ownerShutdown(signum, frame):
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
        with open("files/blacklist.dat", "wb") as blacklist:
            pickle.dump(blacklisted, blacklist)

        await nes.send(f"Rebooting...")
        time.sleep(3)
        python = sys.executable
        os.execl(python, python, *sys.argv)

    else:
        return

@client.command(pass_context = True)
async def help(nes, value: str = None):
    embed = discord.Embed(
        colour = discord.Colour.blue()
    )
    if not value:
        embed.set_author(name = "RosKGB V2.5 - Help")
        embed.add_field(name = "$help error_code", value = "Lists commands for the error codes.", inline = False)
        embed.add_field(name = "$help server", value = "Lists commands for the server.", inline = False)
        embed.add_field(name = "$help voice", value = "Lists commands for the voice.", inline = False)
        embed.add_field(name = "$help other", value = "Lists commands for the voice.", inline = False)
        await nes.send(embed = embed)

    elif value == "error_code":
        embed.set_author(name = "RosKGB V2.5 - Help - Error Code")
        embed.add_field(name = "$bc OR $bugcheck <VALUE>", value = "Gives meaning of bugcheck codes.", inline = False)
        embed.add_field(name = "$hr OR $hresult <VALUE>", value = "Gives meaning of bugcheck codes.", inline = False)
        embed.add_field(name = "$mm OR $ntstatus <VALUE>", value = "Gives meaning of bugcheck codes.", inline = False)
        embed.add_field(name = "$we OR $winerror <VALUE>", value = "Gives meaning of bugcheck codes.", inline = False)
        embed.add_field(name = "$wm OR $windowmessge <VALUE>", value = "Gives meaning of bugcheck codes.", inline = False)
        await nes.send(embed = embed)

    elif value == "server":
        embed.set_author(name = "RosKGB V2.5 - Help - Server")
        embed.add_field(name = "$blacklist <ID>", value = "Blacklists the user from using $pol, $unpol and voice commands (FOR OWNER AND MODERATORS ONLY).", inline = False)
        embed.add_field(name = "$listblacklist", value = "Lists the user ids blacklisted (FOR OWNER AND MODERATORS ONLY).", inline = False)
        embed.add_field(name = "$pol", value = "Gives politics role to you.", inline = False)
        embed.add_field(name = "$unblacklist <ID>", value = "Unblacklists the user from using $pol or voice commands (FOR OWNER AND MODERATORS ONLY).", inline = False)               
        embed.add_field(name = "$unpol", value = "Removes politics role from you.", inline = False)
        await nes.send(embed = embed)

    elif value == "other":
        embed.set_author(name = "RosKGB V2.5 - Help - Other")
        embed.add_field(name = "$hi", value = "Says hello world to you.", inline = False)
        embed.add_field(name = "$quote", value = "Gives some random quote to you.", inline = False)
        await nes.send(embed = embed)

    else:
        await nes.send(f"Invalid choice! Please try again")

if __name__ == "__main__":
    for extension in extensions:
        try:
            client.load_extension(extension)
        except(discord.ClientException, ModuleNotFoundError):
            print(f"Failed to load extension {extension}.")
            traceback.print_exc()

    signal.signal(signal.SIGTSTP, ownerShutdown)

    client.run(token, bot = True, reconnect = True)