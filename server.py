import discord
import os
import pickle
from discord.ext import commands
from discord.utils import get

if os.path.isfile("files/blacklist.dat"):
    try:
        with open("files/blacklist.dat", "rb") as blacklist:
            blacklisted = pickle.load(blacklist)

    except EOFError:
        blacklisted = []

else:
    print("blacklist.dat is either deleted or corrupted! Please check and try again.")

class serverCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role("Admins", "Moderators")
    async def blacklist(self, nes, user_id: str):
        if len(user_id) == 18 and user_id.isdigit():
            if user_id in blacklisted:
                await nes.send(f"User already exists!")

            else:
                blacklisted.append(user_id)
                await nes.send(f"User blacklisted.")

        else:
            await nes.send(f"Invalid User ID! Please try again.")

    @commands.command()
    @commands.has_any_role("Admins", "Moderators")
    async def listblacklist(self, nes):
        listBlacklist = str(blacklisted)[1:-1]

        if not blacklisted:
        	await nes.send(f"No one is blacklisted.")

        else:
            await nes.send("List of User IDs blacklisted -\n`{}`" .format(listBlacklist))

    @commands.command()
    @commands.has_any_role("Admins", "Moderators")
    async def unblacklist(self, nes, type_: str, user_id: str):
        if len(user_id) == 18 and user_id.isdigit():
            if user_id in blacklisted:
                blacklisted.remove(user_id)
                await nes.send(f"User unblacklisted.")

            else:
                await nes.send(f"User doesn't exist! Please try again.")

        else:
            await nes.send(f"Invalid User ID! Please try again.")

    @commands.command()
    async def pol(self, nes):
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

    @commands.command()
    async def unpol(self, nes):
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

def setup(client):
    client.add_cog(serverCog(client))