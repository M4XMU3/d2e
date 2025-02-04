#!/bin/bash

# variables
model="gpt-3.5-turbo-1106"
url="https://api.openai.com/v1/chat/completions"
api_key="*****"
source "$(dirname "$0")/nls-rules.sh"

while read -r LINE; do
     to_translate="$LINE"

     # combine common messages and easy_language_rules
     all_messages=('{"role": "system", "content": "Sie sind ein Übersetzer, welcher Texte, im Kontext der Landeshauptstadt München, in Leichte Sprache übersetzt."}' \
          '{"role": "system", "content": "Die Übersetzungen werden genutzt um den Basistext Menschen mit Behinderung zugänglich zu machen."}' \
          '{"role": "system", "content": "Komposita wie \"Personalausweis\" müssen in z.B. \"Personal-Ausweis\" aufgeteilt werden."}' \
          '{"role": "system", "content": "Falls Beispiele nötig sind um einen Sachverhalt zu erklären, geben Sie maximal drei Beispiele an."}' \
          '{"role": "system", "content": "Bei der Übersetzung bleiben Sie so nahe wie möglich am Inhalt der ursprünglichen Nachricht. Sie erfinden nichts dazu was keine Relation mehr zur ursprünglichen Nachricht hat!"}' \
          '{"role": "system", "content": "Ich nenne Ihnen zunächst alle Regeln die für die Übersetzung in Leichte Sprache eingehalten werden müssen."}' \
          '{"role": "system", "content": "Danach werde ich Ihnen einen Text geben. Dieser muss in Leichte Sprache übersetzt werden. Nun die Regeln:"}' \
          "${easy_language_rules[@]}" \
          '{"role": "user", "content": "Bitte in Leichte Sprache übersetzen und dabei die genannten Regeln einhalten: '"$to_translate"'."}')

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
     echo $translation
     echo "$to_translate;$translation" >> pe_translations.csv
done < to_translate.txt
