#!/bin/bash

for i in 1
do
    while read line
    do
    $line
    sleep $(((RANDOM%10)+1))
    done < googleQuery${i}_test_rel.txt
done