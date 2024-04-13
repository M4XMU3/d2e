#!/bin/bash

while IFS=';' read -r source reference bl em ft pe em_ft em_pe ft_pe em_ft_pe; do
    # python lix.py "$source" "$bl" "$reference" "bl"
    python lix.py "$source" "$em" "$reference" "em"
    # python lix.py "$source" "$ft" "$reference" "ft"
    # python lix.py "$source" "$pe" "$reference" "pe"
    python lix.py "$source" "$em_ft" "$reference" "em-ft"
    python lix.py "$source" "$em_pe" "$reference" "em-pe"
    # python lix.py "$source" "$ft_pe" "$reference" "ft-pe"
    python lix.py "$source" "$em_ft_pe" "$reference" "em-ft-pe"
    # python lix.py "$source" "$reference" "$reference" "human"
done < <(tail -n +2 all-translations.csv)
