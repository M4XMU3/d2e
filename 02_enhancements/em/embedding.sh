#!/bin/bash

while IFS= read -r LINE || [ -n "$LINE" ]
    do python embedding.py "$LINE"
done < to_translate.txt