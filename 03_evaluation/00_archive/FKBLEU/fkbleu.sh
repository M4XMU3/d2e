#!/bin/bash

while IFS=';' read -r source reference bl pe em_t em_p ft peft efp; do
    # python fkbleu.py "$source" "$reference" "$reference" "human"
    python fkbleu.py "$source" "$bl" "$reference" "baseline"
    #python fkbleu.py "$source" "$pe" "$reference" "prompt-engineering"
    #python fkbleu.py "$source" "$em_t" "$reference" "em_texts"
    #python fkbleu.py "$source" "$em_p" "$reference" "em_pages"
    #python fkbleu.py "$source" "$ft" "$reference" "fine-tuning"
    #python fkbleu.py "$source" "$peft" "$reference" "pe-on-ft"
    #python fkbleu.py "$source" "$efp" "$reference" "efp"
done < <(tail -n +2 all-translations.csv)
