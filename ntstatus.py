import untangle

obj = untangle.parse("error_codes/ntstatus.xml")

ntdict = {}

for Ntstatus in obj.NtstatusList.Ntstatus:
    ntdict[Ntstatus['value']] = Ntstatus['text']
