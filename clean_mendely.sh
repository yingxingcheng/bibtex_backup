#!/bin/bash

omit=abstract,mendeley-groups,file,annote,keywords,issn,publisher
sortrules=type,year,key
duplicates=key,doi

bibtex-tidy --omit=$omit --curly --numeric --tab --align=13 --sort=$sortrules --duplicates=$duplicates --no-escape --no-remove-dupe-fields --output="library_cleaned.bib"  library.bib

# from library_cleaned.bib to library_checked.bib
./load_doi.py

bibtex-tidy --omit=$omit --curly --numeric --tab --align=13 --sort=$sortrules --duplicates=$duplicates --no-escape --no-remove-dupe-fields --output="library_checked_cleaned.bib"  library_checked.bib
