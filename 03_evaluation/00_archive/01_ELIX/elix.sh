#!/bin/bash

while IFS=';' read -r source reference bl pe em_t em_p ft peft leo; do
    #python elix.py "$bl" "baseline"
    #python elix.py "$pe" "prompt-engineering"
    #python elix.py "$em_t" "em_texts"
    #python elix.py "$em_p" "em_pages"
    #python elix.py "$ft" "fine-tuning"
    #python elix.py "$peft" "pe-on-ft"
    python elix.py "$leo" "leo"
done < <(tail -n +2 all-translations.csv)
