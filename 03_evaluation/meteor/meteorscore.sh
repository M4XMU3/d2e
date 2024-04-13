#!/bin/bash

while IFS=';' read -r source reference bl em ft pe em_ft em_pe ft_pe em_ft_pe; do
    # python meteorscore.py "$source" "$bl" "$reference" "bl"
    python meteorscore.py "$source" "$em" "$reference" "em"
    # python meteorscore.py "$source" "$ft" "$reference" "ft"
    # python meteorscore.py "$source" "$pe" "$reference" "pe"
    python meteorscore.py "$source" "$em_ft" "$reference" "em-ft"
    python meteorscore.py "$source" "$em_pe" "$reference" "em-pe"
    # python meteorscore.py "$source" "$ft_pe" "$reference" "ft-pe"
    python meteorscore.py "$source" "$em_ft_pe" "$reference" "em-ft-pe"
done < <(tail -n +2 all-translations.csv)
