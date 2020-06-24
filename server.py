import discord
import os
import pickle
import configparser
from discord.ext import commands
from discord.utils import get
from datetime import datetime

if os.path.isfile("files/blacklist.dat"):
    try:
        with open("files/blacklist.dat", "rb") as blacklist:
            blacklisted = pickle.load(blacklist)

    except EOFError:
        blacklisted = {}
    
if os.path.isfile("files/config.ini"):
    config = configparser.ConfigParser()
    config.read("files/config.ini")
    admin_role = config["ROLE_NAMES"]["ADMINISTRATOR"]
    mod_role = config["ROLE_NAMES"]["MODERATOR"]
    politics_role = config["ROLE_NAMES"]["POLITICS"]
    pol_channel_id = int(config["CHANNEL_IDS"]["POLITICS"])
    log_channel_id = int(config["CHANNEL_IDS"]["MOD_LOG"])

else:
    print("config.ini either deleted or corrupted! Please check and try again.")
    sys.exit(0)

class serverCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role(admin_role, mod_role)
    async def polban(self, nes, id: int):
        user_id = str(id)
        author = nes.message.author
        user_name = await nes.guild.fetch_member(id)
        pol_channel = self.client.get_channel(pol_channel_id)
        log_channel = self.client.get_channel(log_channel_id)
        role = get(user_name.guild.roles, name = politics_role)

        if user_id in blacklisted:
            await nes.send("User is already banned!")

        elif user_name == author:
            await nes.send("Don't just ban yourself you nullptr!")
        
        else:
            if role in user_name.roles:
                await user_name.remove_roles(role)

            blacklisted[user_id] = str(user_name)
            with open("files/blacklist.dat", "wb") as blacklist:
                pickle.dump(blacklisted, blacklist)

            for channel in author.guild.channels:
                if channel == log_channel:
                    now = datetime.utcnow()
                    today = now.strftime("%H:%M:%S")
                    await channel.send(f"`[{today}]` :hammer: **{author}** restricted access to {pol_channel.mention} for **{user_name}** (ID:{user_id})")

            await nes.send(f"{user_name} is banned from accessing {pol_channel.mention} channel")

    @commands.command()
    @commands.has_any_role(admin_role, mod_role)
    async def listids(self, nes):
        listBlacklist = str(blacklisted)[1:-1]

        if not blacklisted:
        	await nes.send("No one is banned.")

        else:
            await nes.send(f"List of User IDs banned - `{listBlacklist}`")

    @commands.command()
    @commands.has_any_role(admin_role, mod_role)
    async def polunban(self, nes, id: int):
        user_id = str(id)
        author = nes.message.author
        user_name = await nes.guild.fetch_member(id)
        pol_channel = self.client.get_channel(pol_channel_id)
        log_channel = self.client.get_channel(log_channel_id)

        if user_id in blacklisted:
            del blacklisted[user_id]
            with open("files/blacklist.dat", "wb") as blacklist:
                pickle.dump(blacklisted, blacklist)

            for channel in author.guild.channels:
                if channel == log_channel:
                    now = datetime.utcnow()
                    today = now.strftime("%H:%M:%S")
                    await channel.send(f"`[{today}]` :white_check_mark: **{author}** unrestricted access to {pol_channel.mention} for **{user_name}** (ID:{user_id})")

            await nes.send(f"{user_name} is unbanned from accessing {pol_channel.mention} channel")

        else:
            await nes.send("User doesn't exist! Please try again.")

    @commands.command()
    async def pol(self, nes):
        author = nes.message.author
        id = str(nes.message.author.id)
        role = get(author.guild.roles, name = politics_role)
        pol_channel = self.client.get_channel(pol_channel_id)

        if id in blacklisted:
            await nes.send(f"Sorry, you have been banned from accessing {pol_channel} channel.")
            return

        elif role in author.roles:
            await author.remove_roles(role)
            await nes.send("Role removed from you.")

        else:
            await author.add_roles(role)
            await nes.send("Role assigned to you.")

    @polban.error
    async def polban_error(self, nes, error):
        error = getattr(error, "original", error)
        if isinstance(error,discord.NotFound):
            await nes.send("Invalid User ID! Please try again.")

    @polunban.error
    async def polunban_error(self, nes, error):
        error = getattr(error, "original", error)
        if isinstance(error,discord.NotFound):
            await nes.send("Invalid User ID! Please try again.")

def setup(client):
    client.add_cog(serverCog(client))
