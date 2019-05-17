
import discord
from discord.ext import commands
from discord.utils import get
import logging
import pickle
client = commands.Bot(command_prefix = '$')
client.remove_command('help')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@client.event
async def on_ready():
    print("Bot is online as {0.user}" .format(client))

@client.event
async def on_message(message):
    print(f"{message.channel}: {message.author}: {message.content}")
    await client.process_commands(message)

@client.command(pass_context = True)
async def bugcheck(nes, value: str):
    from bugcheck import bugdict

    if value in bugdict:
        await nes.send("The meaning of this error code is - `{}`" .format(bugdict[value]))

    else:
        await nes.send(f"Error code not found! Please check the code and try again.")

@client.command(pass_context = True)
@commands.has_any_role('Admins', 'Moderators')
async def blacklist(nes, value: str):
    blacklist = open("blacklist.dat", "rb")
    data = pickle.load(blacklist)
    blacklist.close()
    blacklist = open("blacklist.dat", "wb")
    data.append(value)
    pickle.dump(data, blacklist)
    blacklist.close()
    await nes.send(f"User blacklisted.")

@client.command(pass_context = True)
async def help(nes):
    embed = discord.Embed(
        colour = discord.Colour.blue()
    )

    embed.set_author(name = 'BSOD Bot V1.5 - Commands')
    embed.add_field(name = '$bugcheck <VALUE>', value = "Gives meaning of bugcheck codes.", inline = False)
    embed.add_field(name = '$blacklist <VALUE>', value = "(ONLY FOR ADMIN AND MODERATORS) Blacklists an user for usage of $pol command.", inline = False)
    embed.add_field(name = '$unblacklist <VALUE>', value = "(ONLY FOR ADMIN AND MODERATORS) Unblacklists an user for usage of $pol command.", inline = False)
    embed.add_field(name = '$hi', value = "Says hello world to you.", inline = False)
    embed.add_field(name = '$hresult <VALUE>', value = "Gives meaning of hresult codes.", inline = False)
    embed.add_field(name = '$mmresult <VALUE>', value = "Gives meaning of mmresult codes.", inline = False)
    embed.add_field(name = '$ntstatus <VALUE>', value = "Gives meaning of ntstatus codes.", inline = False)
    embed.add_field(name = '$pol', value = "Gives Politics role to you.", inline = False)
    embed.add_field(name = '$winerror <VALUE>', value = "Gives meaning of winerror codes.", inline = False)
    await nes.send(embed = embed)

@client.command(pass_context = True)
async def hi(nes):
    author = nes.message.author.mention
    await nes.send("{} Hello World!" .format(author))

@client.command(pass_context = True)
async def hresult(nes, value: str):
    from hresult import hrdict

    if value in hrdict:
        await nes.send("The meaning of this error code is - `{}`" .format(hrdict[value]))

    else:
        await nes.send(f"Error code not found! Please check the code and try again.")

@client.command(pass_context = True)
async def mmresult(nes, value: str):
    from mmresult import mmdict

    if value in mmdict:
        await nes.send("The meaning of this error code is - `{}`" .format(mmdict[value]))

    else:
        await nes.send(f"Error code not found! Please check the code and try again.")

@client.command(pass_context = True)
async def ntstatus(nes, value: str):
    from ntstatus import ntdict

    if value in ntdict:
        await nes.send("The meaning of this error code is - `{}`" .format(ntdict[value]))

    else:
        await nes.send(f"Error code not found! Please check the code and try again.")

@client.command(pass_context = True)
async def pol(nes):
    blacklist = open("blacklist.dat", "rb")
    data = pickle.load(blacklist)
    blacklist.close()
    author = nes.message.author
    id = str(nes.message.author.id)
    role = get(author.guild.roles, name = "Politics")

    if id in data:
        return

    else:
        await author.add_roles(role)
        await nes.send(f"Role assigned to you.")

@client.command(pass_context = True)
@commands.has_any_role('Admins', 'Moderators')
async def unblacklist(nes, value: str):
    blacklist = open("blacklist.dat", "rb")
    data = pickle.load(blacklist)
    blacklist.close()
    id = str(value)
    
    if id in data:
        blacklist = open("blacklist.dat", "wb")
        data.remove(id)
        pickle.dump(data, blacklist)
        blacklist.close()
        await nes.send(f"User unblacklisted.")

    else:
        await nes.send(f"User doesn't exist! Please try again.")

@client.command(pass_context = True)
async def winerror(nes, value: str):
    from winerror import windict

    if value in windict:
        await nes.send("The meaning of this error code is - `{}`" .format(windict[value]))

    else:
        await nes.send(f"Error code not found! Please check the code and try again.")


client.run('')
