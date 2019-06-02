import untangle

obj = untangle.parse("error_codes/hresult.xml")

hrdict = {}

for Hresult in obj.HresultList.Hresult:
    hrdict[Hresult['value']] = Hresult['text']
