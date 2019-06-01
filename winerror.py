import untangle

obj = untangle.parse("error_codes/winerror.xml")

windict = {}

for Winerror in obj.WinerrorList.Winerror:
    strValue = 8 - len(Winerror['value'])
        
    errorCode = "0" * strValue + Winerror['value']
    
    windict[errorCode] = Winerror['text']