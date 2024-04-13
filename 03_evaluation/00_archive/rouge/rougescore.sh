#!/bin/bash

while IFS=';' read -r source reference bl pe em ft peft efphu efp; do
    # python rougescore.py "$source" "$source" "$reference" "human"
    python rougescore.py "$source" "$bl" "$reference" "baseline"
    python rougescore.py "$source" "$pe" "$reference" "prompt-engineering"
    python rougescore.py "$source" "$em" "$reference" "embedding"
    python rougescore.py "$source" "$ft" "$reference" "fine-tuning"
    python rougescore.py "$source" "$peft" "$reference" "pe-on-ft"
    python rougescore.py "$source" "$efp" "$reference" "efp"
done < <(tail -n +2 all-translations.csv)