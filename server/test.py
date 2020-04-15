#!/usr/bin/python3

import sys
import json

print("Content-type: application/json")
print("")

return_obj = {}
request = sys.stdin.read().split("&")
for r in request:
   key, value = r.split("=")
   return_obj[key] = value

print(json.dumps(return_obj))


