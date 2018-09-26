#!/bin/bash

set -e
set -x

infile=$1

error(){
    echo "Failed: $1"
    exit 13
}

while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "Running on $line"
    sh extract_relevant_gifs.sh $line || error "could not run extract_relevant_gifs"
done < "$infile"
