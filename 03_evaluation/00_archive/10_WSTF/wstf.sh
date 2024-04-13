#!/bin/bash

while IFS=';' read -r source reference bl pe em_t em_p ft peft leo; do
    # python wstf.py ""$bl" "baseline"
    # python wstf.py "$pe" "prompt-engineering"
    python wstf.py "$em_t" "em_texts"
    python wstf.py "$em_p" "em_pages"
    # python wstf.py "$ft" "fine-tuning"
    # python wstf.py "$peft" "pe-on-ft"
    python wstf.py "$leo" "leo"
done < <(tail -n +2 all-translations.csv)
