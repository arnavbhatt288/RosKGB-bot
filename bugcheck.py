import untangle

obj = untangle.parse("error_codes/bugcheck.xml")

bugdict = {}

for BugCheck in obj.BugCheckList.BugCheck:
    bugdict[BugCheck['value']] = BugCheck['text']
