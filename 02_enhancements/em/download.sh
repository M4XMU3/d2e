#!/bin/bash

# Define the CSV file containing 'normal' and 'easy' URLs
csv_file="muenchen-urls.csv"

# Create the "pages" directory if it doesn't exist
mkdir -p pages

# Read the CSV file and download content for each 'normal' and 'easy' URL
while IFS=, read -r normal_url easy_url; do
    # Extract filenames from the URLs
    easy_filename=$(basename "$easy_url" | sed 's/.html$//')  # Extract the base filename from 'easy' URL
    normal_filename=$(echo "$easy_filename" | sed 's/-ls$//')  # Remove "-ls" from 'easy' filename to get 'normal' filename

    # Download the HTML content for "normal" article
    # Use wget to download the HTML content of 'normal' URL
    normal_content=$(wget -qO- "$normal_url" | \
    # Extract content within the main element using awk
    awk '/<main id="content">/,/<\/main>/' | \
    # Remove script elements
    sed '/<script/,/<\/script>/d' | \
    # Remove JavaScript functions
    sed '/function openICalendar(/,/\}/d' | \
    # Remove HTML tags
    sed -e 's/<[^>]*>//g' | \
    # Remove content after specified text
    sed '/Der Text hält sich an die Regeln von Inclusion Europe/,$d' | \
    # Remove leading and trailing whitespace on each line
    sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | \
    # Remove consecutive empty lines, leaving only two
    sed '/^$/N;/^\n$/D')

    # Download the HTML content for "easy" article
    # Use wget to download the HTML content of 'easy' URL
    easy_content=$(wget -qO- "$easy_url" | \
    # Extract content within the main element using awk
    awk '/<main id="content">/,/<\/main>/' | \
    # Remove script elements
    sed '/<script/,/<\/script>/d' | \
    # Remove JavaScript functions
    sed '/function openICalendar(/,/\}/d' | \
    # Remove HTML tags
    sed -e 's/<[^>]*>//g' | \
    # Remove content after specified text
    sed '/Der Text hält sich an die Regeln von Inclusion Europe/,$d' | \
    # Remove leading and trailing whitespace on each line
    sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | \
    # Remove consecutive empty lines, leaving only two
    sed '/^$/N;/^\n$/D')

    # Save the content to files
    echo "$normal_content" > "pages/${normal_filename}.txt"  # Save 'normal' content to file
    echo "$easy_content" > "pages/${easy_filename}.txt"  # Save 'easy' content to file

    # Print a message indicating that text content has been saved for 'normal' and 'easy' articles
    echo "Text content for 'normal' and 'easy' articles has been saved to pages/${normal_filename}.txt and pages/${easy_filename}.txt"

done < "$csv_file"

# Print a message indicating that the download and extraction process is completed
echo "Download and extraction process completed."
