import discord
import os
import pickle
import configparser
from discord.ext import commands
from discord.utils import get

pol_channel_name = "#politics"

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

else:
    print("config.ini either deleted or corrupted! Please check and try again.")
    sys.exit(0)

class serverCog(commands.Cog):
    def __init__(self, client):
        self.client = client
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

        else:
            print("config.ini either deleted or corrupted! Please check and try again.")
            sys.exit(0)

    @commands.command()
    @commands.has_any_role(admin_role, mod_role)
    async def polban(self, nes, id: int):
        user_id = str(id)
        author = await nes.guild.fetch_member(id)
        role = get(author.guild.roles, name = politics_role)
        if len(user_id) > 16 or len(user_id) < 22 and user_id.isdigit():
            if user_id in blacklisted:
                await nes.send(f"User is already banned!")

            else:
                if role in author.roles:
                    await author.remove_roles(role)

                blacklisted[user_id] = str(author)
                with open("files/blacklist.dat", "wb") as blacklist:
                    pickle.dump(blacklisted, blacklist)
                await nes.send(f"User banned from accessing {pol_channel_name} channel")

        else:
            await nes.send(f"Invalid User ID! Please try again.")

    @commands.command()
    @commands.has_any_role(admin_role, mod_role)
    async def listids(self, nes):
        listBlacklist = str(blacklisted)[1:-1]

        if not blacklisted:
        	await nes.send(f"No one is banned.")

        else:
            await nes.send("List of User IDs banned - `{}`" .format(listBlacklist))

    @commands.command()
    @commands.has_any_role(admin_role, mod_role)
    async def polunban(self, nes, user_id: str):
        if len(user_id) == 18 and user_id.isdigit():
            if user_id in blacklisted:
                del blacklisted[user_id]
                with open("files/blacklist.dat", "wb") as blacklist:
                    pickle.dump(blacklisted, blacklist)
                await nes.send(f"User unbanned from accessing {pol_channel_name}  channel")

            else:
                await nes.send(f"User doesn't exist! Please try again.")

        else:
            await nes.send(f"Invalid User ID! Please try again.")

    @commands.command()
    async def pol(self, nes):
        author = nes.message.author
        id = str(nes.message.author.id)
        role = get(author.guild.roles, name = politics_role)

        if id in blacklisted:
            await nes.send(f"Sorry, you have been banned from accessing {pol_channel_name} channel.")
            return

        elif role in author.roles:
            await author.remove_roles(role)
            await nes.send(f"Role removed from you.")

        else:
            await author.add_roles(role)
            await nes.send(f"Role assigned to you.")

def setup(client):
    client.add_cog(serverCog(client))
