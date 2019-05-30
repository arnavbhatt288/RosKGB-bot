
from bugcheck import bugdict
import datetime
import discord
from discord.ext import commands
from discord.utils import get
from hresult import hrdict
import logging
from mmresult import mmdict
from ntstatus import ntdict
import pickle
from winerror import windict
client = commands.Bot(command_prefix = '$')
client.remove_command('help')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

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
    if any(c in value for c in 'x'):
        value = value[2:]

    if len(value) < 8:
        strValue = 8 - len(value)
        value = '0' * strValue + value

    if value in bugdict:
        await nes.send("The meaning of this error code is - `{}`" .format(bugdict[value]))

    else:
        await nes.send(f"Error code not found! Please check the code and try again.")

@client.command(pass_context = True)
async def hresult(nes, value: str):
    if any(c in value for c in 'x'):
        value = value[2:]

    if len(value) < 8:
        strValue = 8 - len(value)
        value = '0' * strValue + value

    if value in hrdict:
        await nes.send("The meaning of this error code is - `{}`" .format(hrdict[value]))

    else:
        await nes.send(f"Error code not found! Please check the code and try again.")

@client.command(pass_context = True)
async def mmresult(nes, value: str):
    if any(c in value for c in 'x'):
        value = value[2:]

    if value.count("0") > 1:
        while len(value) != 0:
            value = value.lstrip('0')
            if len(value) == 2 or len(value) == 1:
                break

    if value in mmdict:
        await nes.send("The meaning of this error code is - `{}`" .format(mmdict[value]))

    else:
        await nes.send(f"Error code not found! Please check the code and try again.")

@client.command(pass_context = True)
async def ntstatus(nes, value: str):
    if any(c in value for c in 'x'):
        value = value[2:]

    if len(value) < 8:
        strValue = 8 - len(value)
        value = '0' * strValue + value

    if value in ntdict:
        await nes.send("The meaning of this error code is - `{}`" .format(ntdict[value]))

    else:
        await nes.send(f"Error code not found! Please check the code and try again.")

@client.command(pass_context = True)
async def winerror(nes, value: str):
    if any(c in value for c in 'x'):
        value = value[2:]

    if value.count("0") > 1:
        while len(value) != 0:
            value = value.lstrip('0')
            if len(value) == 2 or len(value) == 1:
                break

    if value in windict:
        await nes.send("The meaning of this error code is - `{}`" .format(windict[value]))

    else:
        await nes.send(f"Error code not found! Please check the code and try again.")

# Other commands

@client.command(pass_context = True)
@commands.has_any_role('Admins', 'Moderators')
async def blacklist(nes, value: str):
    if len(value) == 18:
        with open("blacklist.dat", "rb") as blacklist:
            data = pickle.load(blacklist)

        if value in data:
            await nes.send(f"User already exists!")

        else:
            with open("blacklist.dat", "wb") as blacklist:
                data.append(value)
                pickle.dump(data, blacklist)
            await nes.send(f"User blacklisted.")

    else:
        await nes.send(f"Invalid User ID! Please try again.")

@client.command(pass_context = True)
async def help(nes):
    embed = discord.Embed(
        colour = discord.Colour.blue()
    )

    embed.set_author(name = 'RosKGB V2.0 - Commands')
    embed.add_field(name = '$bugcheck <VALUE>', value = "Gives meaning of bugcheck codes.", inline = False)
    embed.add_field(name = '$blacklist <VALUE>', value = "(ONLY FOR ADMIN AND MODERATORS) Blacklists an user for usage of $pol and $unpol command.", inline = False)
    embed.add_field(name = '$unblacklist <VALUE>', value = "(ONLY FOR ADMIN AND MODERATORS) Unblacklists an user for usage of $pol and $unpol command.", inline = False)
    embed.add_field(name = '$hi', value = "Says hello world to you.", inline = False)
    embed.add_field(name = '$hresult <VALUE>', value = "Gives meaning of hresult codes.", inline = False)
    embed.add_field(name = '$mmresult <VALUE>', value = "Gives meaning of mmresult codes.", inline = False)
    embed.add_field(name = '$ntstatus <VALUE>', value = "Gives meaning of ntstatus codes.", inline = False)
    embed.add_field(name = '$pol', value = "Gives Politics role to you.", inline = False)
    embed.add_field(name = '$unpol', value = "Removes Politics role from you.", inline = False)
    embed.add_field(name = '$winerror <VALUE>', value = "Gives meaning of winerror codes.", inline = False)
    await nes.send(embed = embed)

@client.command(pass_context = True)
async def hi(nes):
    author = nes.message.author.mention
    await nes.send("{} Hello World!" .format(author))

@client.command(pass_context = True)
async def pol(nes):
    with open("blacklist.dat", "rb") as blacklist:
        data = pickle.load(blacklist)
    author = nes.message.author
    id = str(nes.message.author.id)
    role = get(author.guild.roles, name = "Politics")

    if id in data:
        return

    elif role in author.roles:
        await nes.send(f"You already have the role!")

    else:
        await author.add_roles(role)
        await nes.send(f"Role assigned to you.")

@client.command(pass_context = True)
@commands.has_any_role('Admins', 'Moderators')
async def unblacklist(nes, value: str):
    if len(value) == 18:
        with open("blacklist.dat", "rb") as blacklist:
            data = pickle.load(blacklist)

        if value in data:
            with open("blacklist.dat", "wb") as blacklist:
                data.remove(value)
                pickle.dump(data, blacklist)
            await nes.send(f"User unblacklisted.")

        else:
            await nes.send(f"User doesn't exist! Please try again.")

    else:
        await nes.send(f"Invalid User ID! Please try again.")

@client.command(pass_context = True)
async def unpol(nes):
    with open("blacklist.dat", "rb") as blacklist:
        data = pickle.load(blacklist)
    author = nes.message.author
    id = str(nes.message.author.id)
    role = get(author.guild.roles, name = "Politics")

    if id in data:
        return

    elif not role in author.roles:
        await nes.send(f"You don't already have the role!")

    else:
        await author.remove_roles(role)
        await nes.send(f"Role removed from you.")


client.run('no token')
