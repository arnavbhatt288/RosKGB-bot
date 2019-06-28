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

if os.path.isfile("files/voice_blacklist.dat"):
    try:
        with open("files/voice_blacklist.dat", "rb") as blacklist:
            voice_blacklisted = pickle.load(blacklist)

    except EOFError:
        voice_blacklisted = []

else:
    print("voice_blacklist.dat is either deleted or corrupted! Please check and try again.")

class serverCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role("Admins", "Moderators")
    async def blacklist(self, nes, type_: str, user_id: str):
        if len(user_id) == 18 and user_id.isdigit():
            if user_id in blacklisted:
                await nes.send(f"User already exists!")

            else:
                if type_ == "pol":
                    blacklisted.append(user_id)
                    await nes.send(f"User blacklisted.")

                elif type_ == "voice":
                    voice_blacklisted.append(user_id)
                    await nes.send(f"User blacklisted.")

                elif type_ == "both":
                    blacklisted.append(user_id)
                    voice_blacklisted.append(user_id)
                    await nes.send(f"User blacklisted.")

                else:
                    await nes.send(f"Invalid choice! Please try again.")

        else:
            await nes.send(f"Invalid User ID! Please try again.")

    @commands.command()
    @commands.has_any_role("Admins", "Moderators")
    async def listblacklist(self, nes, type_: str):
        listBlacklist = str(blacklisted)[1:-1]
        list_voiceBlacklist = str(voice_blacklisted)[1:-1]

        if type_ == "pol":
            if not blacklisted:
                await nes.send(f"No one is blacklisted.")

            else:
                await nes.send(f"List of User IDs blacklisted - ")
                await nes.send("`{}`" .format(listBlacklist))

        elif type_ == "voice":
            if not voice_blacklisted:
                await nes.send(f"No one is blacklisted.")

            else:
                await nes.send(f"List of User IDs blacklisted - ")
                await nes.send("`{}`" .format(list_voiceBlacklist))

        else:
            await nes.send(f"Invalid choice! Please try again")

    @commands.command()
    @commands.has_any_role("Admins", "Moderators")
    async def unblacklist(self, nes, type_: str, user_id: str):
        if len(user_id) == 18 and user_id.isdigit():
            if user_id in blacklisted:
                if type_ == "pol":
                    blacklisted.remove(user_id)
                    await nes.send(f"User unblacklisted.")

                elif type_ == "voice":
                    voice_blacklisted.remove(user_id)
                    await nes.send(f"User unblacklisted.")

                elif type_ == "both":
                    blacklisted.remove(user_id)
                    voice_blacklisted.remove(user_id)
                    await nes.send(f"User unblacklisted.")

                else:
                    await nes.send(f"Invalid choice! Please try again.")

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