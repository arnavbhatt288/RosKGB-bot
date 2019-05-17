import untangle

obj = untangle.parse("error_codes/winerror.xml")

windict = {}

for Winerror in obj.WinerrorList.Winerror:
    windict[Winerror['value']] = Winerror['text']