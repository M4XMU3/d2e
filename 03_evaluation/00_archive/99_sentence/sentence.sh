#!/bin/bash

count() {
    # Count newlines
    newline_count=$(echo -e "$1" | grep -c $'\\n')
    # Count sentences (assuming each sentence ends with a period, question mark, or exclamation mark)
    sentence_count=$(echo -e "$1" | grep -E -o '[.!?]' | wc -l)
    # count colons; we want short sentences without colons
    colon_count=$(echo $1 | grep -c ',')

    # newline sentences ratio
    if [ $sentence_count -eq 0 ]; then
	# no sentence ending with punctuation; e.g. a list
        sentence_count=$newline_count
    fi
    nsr=$(echo "scale=2; $newline_count / $sentence_count" | bc)

    # print results
    echo "$newline_count;$sentence_count;$nsr" >> ${2}_sentence_scores.csv
}


while IFS=';' read -r source reference bl pe em ft peft; do
   # python sentence.py "foo!\nba,r.\nba,z?" "baseline"
   python sentence.py "$bl" "baseline"
  # python sentence.py "$pe" "prompt-engineering"
  # python sentence.py "$ft" "fine-tuning"
  # python sentence.py "$peft" "pe-on-ft"
done < <(tail -n +2 all-translations.csv)
