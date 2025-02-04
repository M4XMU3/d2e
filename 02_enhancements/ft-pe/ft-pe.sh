#!/bin/bash

# variables
#first version model="ft:gpt-3.5-turbo-1106:personal::8Nl2nHOu"
model="ft:gpt-3.5-turbo-1106:personal::8csRrLMi"
url="https://api.openai.com/v1/chat/completions"
api_key="*****"
source "$(dirname "$0")/nls-rules.sh"
# to_translate=$1


function translate() {
     # combine common messages and easy_language_rules
     all_messages=('{"role": "system", "content": "Sie sind ein System, welches Texte in leichte Sprache übersetzt."}' \
          '{"role": "user", "content": "Sie sind ein Übersetzer, welcher Texte, im Kontext der Landeshauptstadt München, in leichte Sprache übersetzt."}' \
          '{"role": "user", "content": "Die Übersetzungen werden genutzt um den Basistext Menschen mit Behinderung zugänglich zu machen."}' \
          '{"role": "user", "content": "Komposita wie 'Personalausweis' müssen in z.B. 'Personal-Ausweis' aufgeteilt werden."}' \
          '{"role": "user", "content": "Falls Beispiele nötig sind um einen Sachverhalt zu erklären, geben Sie maximal drei Beispiele an."}' \
          '{"role": "user", "content": "Bei der Übersetzung bleiben Sie so nahe wie möglich am Inhalt der ursprünglichen Nachricht. Sie erfinden nichts dazu was keine Relation mehr zur ursprünglichen Nachricht hat!"}' \
          '{"role": "user", "content": "Ich nenne Ihnen zunächst alle Regeln die für die Übersetzung in leichte Sprache eingehalten werden müssen."}' \
          '{"role": "user", "content": "Danach werde ich Ihnen einen Text geben. Dieser muss in leichte Sprache übersetzt werden. Nun die Regeln:"}' \
          "${easy_language_rules[@]}" \
          '{"role": "user", "content": "Bitte in leichte Sprache übersetzen: '"$to_translate"'."}')

     # send "Leichte Sprache" rules  and to-translate text as single prompts for prompt engineered translation
     ## extract translation from API response with 'jq' at the end
     translation=$(curl -X POST -H "Content-Type: application/json" \
          -H "Authorization: Bearer $api_key" \
          -d '{
          "model": "'"$model"'",
          "messages": '"$(printf '%s\n' "${all_messages[@]}" | jq -s -c .)"'
     }' \
          $url | grep "content" | awk -F'"' '{print $4}')
          # --noproxy '*' $url | grep "content" | awk -F'"' '{print $4}')
     # document translations
     #     --noproxy '*' $url | jq -r '.choices[0].message.content')
     # document translations
     echo -e "$to_translate\n$translation\n------"
     echo "$to_translate;$translation" >> ft-pe-translations.csv
}

while IFS= read -r LINE || [ -n "$LINE" ]
    do translate "$LINE"
done < to_translate.txt
