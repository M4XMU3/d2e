#!/bin/bash

while IFS=';' read -r source reference bl pe em_p ft peft efp; do
    # python nist.py "$source" "$reference" "$reference" "human"
    # python nist.py "$source" "$bl" "$reference" "baseline"
    python nist.py "$source" "$pe" "$reference" "prompt-engineering"
    python nist.py "$source" "$em_t" "$reference" "em_texts"
    python nist.py "$source" "$em_p" "$reference" "em_pages"
    python nist.py "$source" "$ft" "$reference" "fine-tuning"
    python nist.py "$source" "$peft" "$reference" "pe-on-ft"
    python nist.py "$source" "$efp" "$reference" "efp"
done < <(tail -n +2 all-translations.csv)
