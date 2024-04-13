#!/bin/bash

while IFS=';' read -r source reference bl em ft pe em_ft em_pe ft_pe em_ft_pe; do
    # python bert.py "$source" "$bl" "$reference" "bl"
    python bert.py "$source" "$em" "$reference" "em"
    # python bert.py "$source" "$ft" "$reference" "ft"
    # python bert.py "$source" "$pe" "$reference" "pe"
    python bert.py "$source" "$em_ft" "$reference" "em-ft"
    python bert.py "$source" "$em_pe" "$reference" "em-pe"
    # python bert.py "$source" "$ft_pe" "$reference" "ft-pe"
    python bert.py "$source" "$em_ft_pe" "$reference" "em-ft-pe"
done < <(tail -n +2 all-translations.csv)
