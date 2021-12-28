import  json
import pprint

with open("first.chk",'r') as checkpoint:
  a=json.load(checkpoint)
  pprint.pprint(a)

x = []
for z in a:
  x.append(z[0])

with open("tst.chk",'w') as outfile:
   json.dump(x,outfile)
