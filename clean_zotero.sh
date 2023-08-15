
#!/bin/bash

omit=abstract,mendeley-groups,file,annote,keywords
sortrules=type,year,key
duplicates=key,doi

bibtex-tidy --omit=$omit --curly --numeric --tab --align=13 --sort=$sortrules --duplicates=$duplicates --no-escape --no-remove-dupe-fields --output="zotero_library_cleaned.bib"  zotero_library.bib

./check_citation_key.py > check.log
