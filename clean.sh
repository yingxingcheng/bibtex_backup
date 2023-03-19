#!/bin/bash

bibtex-tidy --omit=abstract,mendeley-groups,file,annote,keywords,issn --curly --numeric --tab --align=13 --sort=year,key --duplicates=key,doi --no-escape --no-remove-dupe-fields --output="library_cleaned.bib"  library.bib

# from library_cleaned.bib to library_checked.bib
./load_doi.py

bibtex-tidy --omit=abstract,mendeley-groups,file,annote,keywords,issn,publisher --curly --numeric --tab --align=13 --sort=year,key --duplicates=key,doi --no-escape --no-remove-dupe-fields --output="library_checked_cleaned.bib"  library_checked.bib
