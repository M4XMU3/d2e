#!/bin/bash

while IFS=';' read -r source reference bl em ft pe em_ft em_pe ft_pe em_ft_pe; do
    # python ter.py "$source" "$bl" "$reference" "bl"
    python ter.py "$source" "$em" "$reference" "em"
    # python ter.py "$source" "$ft" "$reference" "ft"
    # python ter.py "$source" "$pe" "$reference" "pe"
    python ter.py "$source" "$em_ft" "$reference" "em-ft"
    python ter.py "$source" "$em_pe" "$reference" "em-pe"
    # python ter.py "$source" "$ft_pe" "$reference" "ft-pe"
    python ter.py "$source" "$em_ft_pe" "$reference" "em-ft-pe"
done < <(tail -n +2 all-translations.csv)
