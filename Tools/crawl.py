#!/usr/bin/env python3

import urllib.request
import re

from getConfig import get_value, load_configs


def makeRequest(url):

    request = urllib.request.Request(url)
    with urllib.request.urlopen(request) as response:
        return response.read().decode("utf-8")

    return ""


load_configs()

items = get_value("crawl", [])

for item in items:
	resp = makeRequest(item['url'])
	if re.search(item['match'], resp):
		print("Item " + item['url'] + ":\n\tMatched!")
	else:
		print("Item " + item['url'] + ":\n\tDid not match.")
