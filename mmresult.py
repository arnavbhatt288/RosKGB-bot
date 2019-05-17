import untangle

obj = untangle.parse("error_codes/mmresult.xml")

mmdict = {}

for Mmresult in obj.MmresultList.Mmresult:
    mmdict[Mmresult['value']] = Mmresult['text']