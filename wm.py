import untangle

obj = untangle.parse("error_codes/wm.xml")

wmdict = {}

for Wm in obj.WindowMessageList.WindowMessage:
    strValue = 8 - len(Wm['value'])
    errorCode = "0" * strValue + Wm['value']

    wmdict[errorCode] = Wm['text']
