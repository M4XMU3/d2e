#!/bin/bash

while IFS=';' read -r source reference bl em ft pe em_ft em_pe ft_pe em_ft_pe; do
    # python sari.py "$source" "$bl" "$reference" "bl"
    # python sari.py "$source" "$em" "$reference" "em"
    python sari.py "$source" "$ft" "$reference" "ft"
    # python sari.py "$source" "$pe" "$reference" "pe"
    # python sari.py "$source" "$em_ft" "$reference" "em-ft"
    # python sari.py "$source" "$em_pe" "$reference" "em-pe"
    # python sari.py "$source" "$ft_pe" "$reference" "ft-pe"
    # python sari.py "$source" "$em_ft_pe" "$reference" "em-ft-pe"
done < <(tail -n +2 all-translations.csv)
