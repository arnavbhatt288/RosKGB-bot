# id 574562317384024065
# token NTc0NTYyMzE3Mzg0MDI0MDY1.XM7TYg.BLvLtvtzbfDZFcv5ZavUl8C7oxc
# https://discordapp.com/oauth2/authorize?client_id=574562317384024065&scope=bot&permissions=67584

import discord
from discord.ext import commands
import logging
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
    await nes.send("The meaning of this error code is - `{}`" .format(bugdict[value]))

@client.command(pass_context = True)
async def hresult(nes, value: str):
    from hresult import hrdict
    await nes.send("The meaning of this error code is - `{}`" .format(hrdict[value]))

@client.command(pass_context = True)
async def ntstatus(nes, value: str):
    from ntstatus import ntdict
    await nes.send("The meaning of this error code is - `{}`" .format(ntdict[value]))

@client.command(pass_context = True)
async def winerror(nes, value: str):
    from winerror import windict
    await nes.send("The meaning of this error code is - `{}`" .format(windict[value]))

@client.command(pass_context = True)
async def hi(nes):
    author = nes.message.author.mention
    await nes.send("{} Hello World!" .format(author))

@client.command(pass_context = True)
async def about(nes):
    await nes.send(f"```Error Bot v0.5 Codename - Awakening```")

@client.command(pass_context = True)
async def help(nes):
    author = nes.message.author.mention
    
    embed = discord.Embed(
        colour = discord.Colour.blue()
    )
    
    embed.set_author(name = 'Misc')
    embed.add_field(name = '$hi', value = "Says hello world to you!", inline = False)
    embed.add_field(name = '$about', value = "Tells you about the version of bot.", inline = False)
    await nes.send("{} Here are commands below -" .format(author))
    await nes.send(embed = embed)


client.run('NTc0NTYyMzE3Mzg0MDI0MDY1.XM7TYg.BLvLtvtzbfDZFcv5ZavUl8C7oxc')
