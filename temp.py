import xmltodict
import json

with open('input\\TXC Export-FYOR-York_2020-03-15-Uni Holidays.xml') as fd:
    doc = xmltodict.parse(fd.read())

print(json.dumps(doc, indent=4))
print('Done')