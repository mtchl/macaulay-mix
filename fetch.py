#!/usr/bin/env python

"""
For collecting information about audio available from the Macaulay Library.
This script and the data directory could be removed if they offered an 
API of some kind that provides json-p or CORS access.
"""

import os
import re
import json
import time
import urllib

from bs4 import BeautifulSoup

id = 0

while True:
    id += 1
    print(id)

    url = "http://macaulaylibrary.org/audio/%s" % id
    try:
        doc = BeautifulSoup(urllib.urlopen(url), 'xml')
    except IOError:
        id -= 1
        continue

    title = doc.find('meta', {'property': 'og:title'})
    if not title and id < 148984:
        continue

    title = title['content'].strip()
    if ':' in title:
        title = title.split(':', 1)[1].strip()
    data = {"title": title, "url": url}

    for d in doc.find_all('ul', {'class': 'datas'}):
        k = d.find('div', {'class': 'datas-header'})
        v = d.find('li')
        if k and v:
            k = k.text.replace(" ", "_").lower()
            v = v.text.replace("\n", " ").strip()
            v = re.sub(r' +', ' ', v)
            data[k] = v

    # write the data
    prefix = id / 10000
    dir = os.path.join("data", str(prefix))
    if not os.path.isdir(dir):
        os.mkdir(dir)
    path = os.path.join(dir, "%s.json" % id)
    json.dump(data, open(path, "w"), indent=2)

    time.sleep(1)
