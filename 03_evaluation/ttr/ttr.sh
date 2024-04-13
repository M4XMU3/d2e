#!/bin/bash

while IFS=';' read -r source reference bl em ft pe em_ft em_pe ft_pe em_ft_pe; do
    # python ttr.py "$source" "$bl" "$reference" "bl"
    python ttr.py "$source" "$em" "$reference" "em"
    # python ttr.py "$source" "$ft" "$reference" "ft"
    # python ttr.py "$source" "$pe" "$reference" "pe"
    python ttr.py "$source" "$em_ft" "$reference" "em-ft"
    python ttr.py "$source" "$em_pe" "$reference" "em-pe"
    # python ttr.py "$source" "$ft_pe" "$reference" "ft-pe"
    python ttr.py "$source" "$em_ft_pe" "$reference" "em-ft-pe"
    python ttr.py "$source" "$reference" "$reference" "human"
done < <(tail -n +2 all-translations.csv)
