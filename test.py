#!/usr/bin/env python

import json
import Engine
import sys

if len(sys.argv) != 4:
    print("Usage: test.py 'file' 'query' 'pages'")
    exit(1)

TEXT=sys.argv[2]
PAGES=int(sys.argv[3])

provider_file = open(sys.argv[1],"r")
provider = json.loads(provider_file.read())
provider_file.close()

e = Engine.Engine(debug=True)

def callback(data,providerName,nitems):
    for op,values in data.items():
        print("_____________________________________________________")
        print("op:" + op + " #:"+ str(len(values)))
        print(values)
    
    if nitems == 0:
        return

    print("_____________________________________________________")
    if "urls" in provider["ops"] and "crawler" in provider["ops"]["urls"]:
        print("URL crawler detected!")
        print("URL crawler result is '" + e.crawl(provider["baseUrl"],data["urls"][0],provider["ops"]["urls"]["crawler"],provider["headers"] if "headers" in provider else None) + "'")

    print("_____________________________________________________")    
    if "magnets" in provider["ops"] and "crawler" in provider["ops"]["magnets"]:
        print("MAGNET crawler detected!")
        print("MAGNET crawler result is '" + e.crawl(provider["baseUrl"],data["magnets"][0],provider["ops"]["magnets"]["crawler"],provider["headers"] if "headers" in provider else None) + "'")
    print("_____________________________________________________")


e.makeQuery(provider,TEXT,"All",PAGES,perPageCallback=callback)


print("TEST ENDED")
