import discord
import untangle
from discord.ext import commands

class errorCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["bugcheck", "bc"])
    async def buc(self, nes, value: str):
        obj = untangle.parse("error_codes/bugcheck.xml")

        bugdict = {}

        for BugCheck in obj.BugCheckList.BugCheck:
            bugdict[BugCheck['value']] = BugCheck['text']

        if any(c in value for c in "x"):
            value = value[2:]

        if len(value) < 8:
            strValue = 8 - len(value)
            value = "0" * strValue + value

        if value in bugdict:
            await nes.send("The meaning of this error code is - `{}`" .format(bugdict[value]))

        else:
            await nes.send(f"Error code not found! Please check the code and try again.")

    @commands.command(aliases = ["hresult", "hr"])
    async def hre(self, nes, value: str):
        obj = untangle.parse("error_codes/hresult.xml")

        hrdict = {}

        for Hresult in obj.HresultList.Hresult:
            hrdict[Hresult['value']] = Hresult['text']

        if any(c in value for c in "x"):
            value = value[2:]

        if len(value) < 8:
            strValue = 8 - len(value)
            value = "0" * strValue + value

        if value in hrdict:
            await nes.send("The meaning of this error code is - `{}`" .format(hrdict[value]))

        else:
            await nes.send(f"Error code not found! Please check the code and try again.")

    @commands.command(aliases = ["mmresult", "mm"])
    async def mmr(self, nes, value: str):
        obj = untangle.parse("error_codes/mmresult.xml")

        mmdict = {}

        for Mmresult in obj.MmresultList.Mmresult:
            mmdict[Mmresult['value']] = Mmresult['text']

        if any(c in value for c in "x"):
            value = value[2:]

        if len(value) < 8:
            strValue = 8 - len(value)
            value = "0" * strValue + value

        if value in mmdict:
            await nes.send("The meaning of this error code is - `{}`" .format(mmdict[value]))

        else:
            await nes.send(f"Error code not found! Please check the code and try again.")

    @commands.command(aliases = ["ntresult", "nt"])
    async def ntr(self, nes, value: str):
        obj = untangle.parse("error_codes/ntstatus.xml")

        ntdict = {}

        for Ntstatus in obj.NtstatusList.Ntstatus:
            ntdict[Ntstatus['value']] = Ntstatus['text']

        if any(c in value for c in "x"):
            value = value[2:]

        if len(value) < 8:
            strValue = 8 - len(value)
            value = "0" * strValue + value

        if value in ntdict:
            await nes.send("The meaning of this error code is - `{}`" .format(ntdict[value]))

        else:
            await nes.send(f"Error code not found! Please check the code and try again.")

    @commands.command(aliases = ["winerror", "we"])
    async def wie(self, nes, value: str):
        obj = untangle.parse("error_codes/winerror.xml")

        windict = {}

        for Winerror in obj.WinerrorList.Winerror:
            strValue = 8 - len(Winerror['value'])
            errorCode = "0" * strValue + Winerror['value']

            windict[errorCode] = Winerror['text']

        if any(c in value for c in "x"):
            value = value[2:]

        if len(value) < 8:
            strValue = 8 - len(value)
            value = "0" * strValue + value

        if value in windict:
            await nes.send("The meaning of this error code is - `{}`" .format(windict[value]))

        else:
            await nes.send(f"Error code not found! Please check the code and try again.")

    @commands.command(aliases = ["windowmessage", "wm"])
    async def wme(self, nes, value: str):
        obj = untangle.parse("error_codes/wm.xml")

        wmdict = {}

        for Wm in obj.WindowMessageList.WindowMessage:
            strValue = 8 - len(Wm['value'])
            errorCode = "0" * strValue + Wm['value']

            wmdict[errorCode] = Wm['text']

        if any(c in value for c in "x"):
            value = value[2:]

        if len(value) < 8:
            strValue = 8 - len(value)
            value = "0" * strValue + value

        if value in wmdict:
            await nes.send("The meaning of this error code is - `{}`" .format(wmdict[value]))

        else:
            await nes.send(f"Error code not found! Please check the code and try again.")

def setup(client):
    client.add_cog(errorCog(client))