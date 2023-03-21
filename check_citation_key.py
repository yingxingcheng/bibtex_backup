#!/usr/bin/env python
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import json


def load_db(bib_filename="library.bib", is_cleaned=True):
    if is_cleaned:
        bibfilename = bib_filename.split(".bib")[0] + "_cleaned.bib"

    with open(bibfilename, "r") as f:
        db = bibtexparser.load(f)
    return db


def main():
    mendely_db = load_db(bib_filename="library.bib")
    zotero_db = load_db(bib_filename="zotero_library.bib")
    nb_zotero_db = len(zotero_db.entries)
    print(f"Total number of entries in zotero database: {nb_zotero_db}")

    mendely_dois = {i["doi"].lower(): i["ID"] for i in mendely_db.entries if "doi" in i}
    zotero_dois = {i["doi"].lower(): i["ID"] for i in zotero_db.entries if "doi" in i}

    nb_mdois = len(mendely_dois)
    nb_zdois = len(zotero_dois)
    print(f"Total number of entires containg DOIs in mendely: {nb_mdois}")
    print(f"Total number of entires containg DOIs in zotero: {nb_zdois} \n")

    total_count, correct_count = 0, 0
    key_map = {}
    for doi, z_cite_key in zotero_dois.items():
        if doi not in mendely_dois:
            continue
        m_cite_key = mendely_dois[doi]
        if z_cite_key == m_cite_key:
            correct_count += 1
        else:
            print(m_cite_key, "==>", z_cite_key)
            key_map[m_cite_key] = z_cite_key
        total_count += 1
    print()
    print(f"Correct citation key: {correct_count}/{total_count}")

    with open("key_map.json", "w") as f:
        json.dump(key_map, f)


if __name__ == "__main__":
    main()
