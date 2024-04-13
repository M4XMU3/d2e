#!/bin/bash

while IFS=';' read -r source reference bl em ft pe em_ft em_pe ft_pe em_ft_pe; do
    python snlr.py "$source" "$bl" "$reference" "bl"
    python snlr.py "$source" "$em" "$reference" "em"
    python snlr.py "$source" "$ft" "$reference" "ft"
    python snlr.py "$source" "$pe" "$reference" "pe"
    python snlr.py "$source" "$em_ft" "$reference" "em-ft"
    python snlr.py "$source" "$em_pe" "$reference" "em-pe"
    python snlr.py "$source" "$ft_pe" "$reference" "ft-pe"
    python snlr.py "$source" "$em_ft_pe" "$reference" "em-ft-pe"
    python snlr.py "$source" "$reference" "$reference" "human"
done < <(tail -n +2 all-translations.csv)
