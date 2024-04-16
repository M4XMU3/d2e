#!/bin/bash

# variables
model="text-embedding-ada-002"
url="https://api.openai.com/v1/embeddings"
page=$1
api_key=$(export $(xargs .env) && env | grep OPENAI_API_KEY | awk -F'=' '{print $2}')
vector=$(curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer $api_key" \
     -d '{
	"input": "'"cat $page"'",
	"model": "'"$model"'"
    }' \
    --noproxy '*' $url | jq -r '.' | tr -d '    ' | tr '\n' ' ')
echo -e $vector
echo "$page;$vector" >> em-vectors.csv
