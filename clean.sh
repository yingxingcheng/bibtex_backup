#!/bin/bash

bibtex-tidy --omit=abstract,mendeley-groups,file,annote,keywords --curly --numeric --tab --align=13 --sort=year,key --duplicates=key,doi --no-escape --no-remove-dupe-fields --output="library_cleaned.bib"  library.bib

./load_doi.py
