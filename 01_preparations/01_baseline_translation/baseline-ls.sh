#!/bin/bash

# variables
model="gpt-3.5-turbo-1106"
url="https://api.openai.com/v1/chat/completions"
api_key="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"
to_translate=$1

# combine common messages and easy_language_rules
#all_messages=('{"role": "system", "content": "Sie sind ein System, welches Texte in leichte Sprache übersetzt."}' \
all_messages=('{"role": "user", "content": "Bitte in leichte Sprache übersetzen: '"$to_translate"'."}')

## extract translation from API response with 'jq' at the end
translation=$(curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer $api_key" \
     -d '{
	"model": "'"$model"'",
        "messages": '"$(printf '%s\n' "${all_messages[@]}" | jq -s -c .)"'
    }' \
     --noproxy '*' $url | grep "content" | awk -F'"' '{print $4}')
echo $translation
echo "$to_translate;$translation" >> baseline-translations.csv
