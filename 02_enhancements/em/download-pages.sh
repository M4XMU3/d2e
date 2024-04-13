#!/bin/bash

csv_file="muenchen-urls.csv"

# Create the "pages" directory if it doesn't exist
mkdir -p pages

# Read the CSV file and download content for each 'normal' and 'easy' URL
while IFS=, read -r normal_url easy_url; do
    # Skip the first row (header)
    if [[ "$normal_url" == "normal_url" ]]; then
        continue
    fi

    # Extract filenames from the URLs
    easy_filename=$(basename "$easy_url" | sed 's/.html$//')
    normal_filename=$(echo "$easy_filename" | sed 's/-ls$//')

    # Download the HTML content for "normal" article
    normal_content=$(wget -qO- "$normal_url" | \
        awk '/<main id="content">/,/<\/main>/' | \
        sed '/<script/,/<\/script>/d' | \
        sed '/function openICalendar(/,/\}/d' | \
        sed -e ':a;N;$!ba;s/<style>[^<]*<\/style>//g' | \
        sed -e ':a;N;$!ba;s/<div[^>]*>//g' | \
        sed -e ':a;N;$!ba;s/<img[^>]*>//g' | \
        sed -e ':a;N;$!ba;s/<input[^>]*>//g' | \
        sed -e 's/<[^>]*>//g' | \
        sed '/Der Text hält sich an die Regeln von Inclusion Europe/,$d' | \
        sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | \
        sed '/^$/N;/^\n$/D'
    )

    # Download the HTML content for "easy" article
    easy_content=$(wget -qO- "$easy_url" | \
        awk '/<main id="content">/,/<\/main>/' | \
        sed '/<script/,/<\/script>/d' | \
        sed '/function openICalendar(/,/\}/d' | \
        sed -e ':a;N;$!ba;s/<style>[^<]*<\/style>//g' | \
        sed -e ':a;N;$!ba;s/<div[^>]*>//g' | \
        sed -e ':a;N;$!ba;s/<img[^>]*>//g' | \
        sed -e ':a;N;$!ba;s/<input[^>]*>//g' | \
        sed -e 's/<[^>]*>//g' | \
        sed '/Der Text hält sich an die Regeln von Inclusion Europe/,$d' | \
        sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | \
        sed '/^$/N;/^\n$/D'
    )

    # Save the content to files
    echo "$normal_content" > "pages/${normal_filename}.txt"
    echo "$easy_content" > "pages/${easy_filename}.txt"

    echo "Text content for 'normal' and 'easy' articles has been saved to pages/${normal_filename}.txt and pages/${easy_filename}.txt"

done < "$csv_file"

echo "Download and extraction process completed."

