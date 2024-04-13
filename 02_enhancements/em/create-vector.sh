#!/bin/bash

# variables
model="text-embedding-ada-002"
url="https://api.openai.com/v1/embeddings"
api_key="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"
page=$1

vector=$(curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer $api_key" \
     -d '{
	"input": "'"cat $page"'",
	"model": "'"$model"'"
    }' \
    --noproxy '*' $url | jq -r '.' | tr -d '    ' | tr '\n' ' ')
echo -e $vector
echo "$page;$vector" >> em-vectors.csv
