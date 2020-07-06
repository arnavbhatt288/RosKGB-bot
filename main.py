import discord
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

bot_prefix = "!"

client = commands.Bot(command_prefix = bot_prefix)
client.remove_command("help")

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

extensions = ["server", "error_code"]


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Type !help"))
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
            await channel.send(f"Hello {author} and welcome to the {server} server!\n\nPlease read the community server rules at {rules_channel.mention}! If you want a general overview of what ReactOS is, please take a look at {readme_channel.mention}! Are you confused about the server's channels or role management? Consult {instructional_channel.mention}!")

@client.command(pass_context = True)
async def shutdown(nes):
    if str(nes.message.author.id) == server_owner_id:
        await nes.send("Shutting down...")
        time.sleep(3)
        sys.exit(0)

    else:
        return

@client.command(pass_context = True)
async def reboot(nes):
    if str(nes.message.author.id) == server_owner_id:
        await nes.send("Rebooting...")
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
        embed.set_author(name = "RosKGB V1.0 - Help")
        embed.add_field(name = f"{bot_prefix}help error_code", value = "Lists commands for the error codes.", inline = False)
        embed.add_field(name = f"{bot_prefix}help server", value = "Lists commands for the server.", inline = False)
        await nes.send(embed = embed)

    elif value == "error_code":
        embed.set_author(name = "RosKGB V1.0 - Help - Error Code")
        embed.add_field(name = f"{bot_prefix}bc OR {bot_prefix}bugcheck <VALUE>", value = "Gives meaning of bugcheck codes.", inline = False)
        embed.add_field(name = f"{bot_prefix}hr OR {bot_prefix}hresult <VALUE>", value = "Gives meaning of bugcheck codes.", inline = False)
        embed.add_field(name = f"{bot_prefix}mm OR {bot_prefix}multimedia <VALUE>", value = "Gives meaning of bugcheck codes.", inline = False)
       	embed.add_field(name = f"{bot_prefix}nt OR {bot_prefix}ntresult  <VALUE>", value = "Gives meaning of bugcheck codes.", inline = False)
        embed.add_field(name = f"{bot_prefix}win32 OR {bot_prefix}winerror <VALUE>", value = "Gives meaning of bugcheck codes.", inline = False)
        embed.add_field(name = f"{bot_prefix}wm OR {bot_prefix}windowmessge <VALUE>", value = "Gives meaning of bugcheck codes.", inline = False)
        await nes.send(embed = embed)

    elif value == "server":
        embed.set_author(name = "RosKGB V1.0 - Help - Server")
        embed.add_field(name = f"{bot_prefix}polban <ID>", value = f"Bans the user from using {bot_prefix}pol. (FOR ADMINS AND MODERATORS ONLY).", inline = False)
        embed.add_field(name = f"{bot_prefix}listids", value = f"Lists the user ids banned for using {bot_prefix}pol. (FOR ADMINS AND MODERATORS ONLY).", inline = False)
        embed.add_field(name = f"{bot_prefix}pol", value = "Gives politics role to you.", inline = False)
        embed.add_field(name = f"{bot_prefix}polunban <ID>", value = f"Unbans the user from using {bot_prefix}pol. (FOR ADMINS AND MODERATORS ONLY).", inline = False)
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

    else:
        print("config.ini either deleted or corrupted! Please check and try again.")
        sys.exit(0)

    client.run(token, bot = True, reconnect = True)
