#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
    sh extract_relevant_gifs.sh $line"
done < "$1"
