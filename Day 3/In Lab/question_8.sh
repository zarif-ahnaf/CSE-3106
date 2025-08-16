#!/bin/bash

for num in {1..50}; do
    if (( num % 2 == 0 )); then
        echo "$num is even."
    fi
done