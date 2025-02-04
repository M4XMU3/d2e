#!/bin/bash

# variables
#model="ft:gpt-3.5-turbo-1106:personal::8Nl2nHOu"
model="ft:gpt-3.5-turbo-1106:personal::8csRrLMi"
url="https://api.openai.com/v1/chat/completions"
api_key="*****"
to_translate=$1

all_messages=('{"role": "user", "content": "Bitte in leichte Sprache übersetzen: '"$to_translate"'."}')


# send "Leichte Sprache" rules  and to-translate text as single prompts for prompt engineered translation
## extract translation from API response with 'jq' at the end
translation=$(curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer $api_key" \
     -d '{
	"model": "'"$model"'",
        "messages": '"$(printf '%s\n' "${all_messages[@]}" | jq -s -c .)"'
     }' \
     --noproxy '*' $url | grep "content" | awk -F'"' '{print $4}')
#     --noproxy '*' $url | jq -r '.choices[0].message.content')
# document translations
echo $translation
echo "$to_translate;$translation" >> ft-translations.csv
