import os
import json
from sys import argv


file_in = argv[1]
file_out = argv[2]

f = open(file_in, 'r')
data = json.load(f)
notifiers = set()
res = [x['id'] for x in data if x['notifier'] not in notifiers and not notifiers.add(x['notifier'])]
f = open(file_out, 'w')
for item in res:
	f.write("%s\n" % item)
