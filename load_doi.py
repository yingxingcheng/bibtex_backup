#!/usr/bin/env python

import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import json
from habanero import cn


def load_mendely_db(bib_filename="library.bib", is_cleaned=True):
    if is_cleaned:
        bibfilename = bib_filename.split(".bib")[0] + "_cleaned.bib"

    with open(bibfilename, "r") as f:
        mendely_db = bibtexparser.load(f)
    return mendely_db


def load_online_metadata(dois, json_cache_filename="doi_db.json"):
    with open(json_cache_filename, "r") as f:
        try:
            doi_json = json.load(f)
        except json.decoder.JSONDecodeError:
            doi_json = {}

    count = 1
    for doi in dois:
        if doi in doi_json:
            count += 1
            print(f"{doi:<50} exists, skip it!")
            continue
        try:
            bibtex = cn.content_negotiation(ids=doi)
        except:
            print(f"ERROR: wrong {doi}!")
            count += 1
            continue

        doi_json[doi] = bibtex
        print(f"{count} done!")
        count += 1

    nb_dois = len(dois)
    nb_search = len(doi_json)
    print(f"The number of input dois: {nb_dois}")
    print(f"The number of input dois: {nb_search}")

    with open(json_cache_filename, "w") as f:
        json.dump(doi_json, f)

    # {'doi1': bibtex1, 'doi2':bibtex2}
    return doi_json


def check_mendely(mendely_db, doi_json, verbose=False):
    corrected_entries = []
    # checed_keys = ["year", "volume", "pages"]
    checed_keys = ["year"]
    for mb in mendely_db.entries:
        if "doi" in mb:
            doi = mb["doi"].lower()
            ob = bibtexparser.loads(doi_json[doi]).entries[0]
            ob["ID"] = mb["ID"]
            if verbose:
                print("Mendely bibentry:")
                print(mb)
                print("Online bibentry:")
                print(ob)
                print("Mendely has but online db does not:")
                print(set(mb.keys()) - set(ob.keys()))
                print("Online db has but mendely does not:")
                print(set(ob.keys()) - set(mb.keys()))

            if ob["ENTRYTYPE"] == "article":
                for key in checed_keys:
                    if key not in ob and key not in mb:
                        continue
                    elif key not in ob or key not in mb:
                        print(f"Difference found: {ob['ID']}")
                        break
                    elif ob[key] != mb[key]:
                        print(f"Difference found: {ob['ID']}")
                        break
        else:
            ob = mb
        corrected_entries.append(ob)
    return corrected_entries


def write_bibtex(corrected_entries):
    # TODO: write a list of dict to bibtex
    db = BibDatabase()
    db.entries = corrected_entries
    writer = BibTexWriter()
    with open("library_checked.bib", "w") as bibfile:
        bibfile.write(writer.write(db))


if __name__ == "__main__":
    mendely_db = load_mendely_db()
    dois = [i["doi"].lower() for i in mendely_db.entries if "doi" in i]
    doi_json = load_online_metadata(dois)
    corrected_entries = check_mendely(mendely_db, doi_json)
    write_bibtex(corrected_entries)
