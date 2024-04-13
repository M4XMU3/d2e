#!/bin/bash

while IFS=';' read -r source reference bl pe em_t em_p ft peft leo; do
    # python glix.py "$bl" "baseline"
    # python glix.py "$pe" "prompt-engineering"
    python glix.py "$em_t" "em_texts"
    python glix.py "$em_p" "em_pages"
    # python glix.py "$ft" "fine-tuning"
    # python glix.py "$peft" "pe-on-ft"
    python glix.py "$leo" "leo"
done < <(tail -n +2 all-translations.csv)
