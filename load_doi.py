#!/usr/bin/env python

import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
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


new_db = []
for old_bib in old_db.entries:
    if "doi" in old_bib:
        doi = old_bib["doi"].lower()
        new_bib = bibtexparser.loads(res[doi]).entries[0]
        print(new_bib)
        print(old_bib)
        new_bib["ID"] = old_bib["ID"]
        print(new_bib)
        print(set(old_bib.keys()) - set(new_bib.keys()))
        print(set(new_bib.keys()) - set(old_bib.keys()))
    else:
        new_bib = old_bib
    new_db.append(new_bib)

# TODO: write a list of dict to bibtex
db = BibDatabase()
db.entries = new_db
writer = BibTexWriter()
with open("library_checked.bib", "w") as bibfile:
    bibfile.write(writer.write(db))
