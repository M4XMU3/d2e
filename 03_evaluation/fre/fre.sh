#!/bin/bash

while IFS=';' read -r source reference bl em ft pe em_ft em_pe ft_pe em_ft_pe; do
    # python fre.py "$source" "$bl" "$reference" "bl"
    python fre.py "$source" "$em" "$reference" "em"
    # python fre.py "$source" "$ft" "$reference" "ft"
    # python fre.py "$source" "$pe" "$reference" "pe"
    python fre.py "$source" "$em_ft" "$reference" "em-ft"
    python fre.py "$source" "$em_pe" "$reference" "em-pe"
    # python fre.py "$source" "$ft_pe" "$reference" "ft-pe"
    python fre.py "$source" "$em_ft_pe" "$reference" "em-ft-pe"
    # python fre.py "$source" "$reference" "$reference" "human"
done < <(tail -n +2 all-translations.csv)
