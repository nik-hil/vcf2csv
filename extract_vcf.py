import re
import pandas as pd

files = open(sys.argv[1], "r").read()

contacts = []
matches = re.findall(r"BEGIN:VCARD(.*?)END:VCARD", files, re.S)
for match in matches:
    if "CHARSET=UTF-8;ENCODING=QUOTED-" in match:
        # other than english
        print(re.findall(r"TEL;.*?:(?P<cell>[\d+ ]+)", match))
        continue
    name = {}
    # get name
    val = re.search(r"N:(?P<fname>[A-Za-z0-9 ]+)?;(?P<lname>[A-Za-z0-9 ]+)?", match)
    if val:
        name["fname"] = val["fname"]
        name["lname"] = val["lname"]
    # cell phone
    vals = re.findall(r"TEL;.*?:(?P<cell>[\d+ \+-]+)", match)
    if vals:
        for i, val in enumerate(vals):
            name["cell-"+str(i) ] = val.replace(" ","").replace("-","")
    contacts.append(name)

# print(contacts)
df = pd.DataFrame(contacts)
df.to_csv(sys.argv[1]+".csv")
