#!/usr/bin/env python

import bibtexparser
import json
from habanero import cn


with open("library_cleaned.bib", "r") as f:
    old_db = bibtexparser.load(f)

# dois = {i["doi"].lower() for i in old_db.entries if "doi" in i}
dois = [i["doi"].lower() for i in old_db.entries if "doi" in i]

db_json = "doi_db.json"
with open(db_json, "r") as f:
    try:
        res = json.load(f)
    except json.decoder.JSONDecodeError:
        res = {}

count = 1
for doi in dois:
    if doi in res:
        count += 1
        print(f"{doi:<50} exists, skip it!")
        continue
    try:
        bibtex = cn.content_negotiation(ids=doi)
    except:
        print(f"ERROR: wrong {doi}!")
        count += 1
        continue

    res[doi] = bibtex
    print(f"{count} done!")
    count += 1

print(len(dois))
print(len(res))

with open(db_json, "w") as f:
    json.dump(res, f)
