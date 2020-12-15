import json
import os.path

g = open(os.path.dirname(__file__) + '/isthisall.json')
f = json.load(g)[0]

count = 0
for i in f.keys():
    count += 1

print(count)