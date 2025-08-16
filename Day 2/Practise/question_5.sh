#!/bin/bash
input=""

until [ "$input" == "exit" ]; do
    read -p "Enter something (type 'exit' to quit): " input
    echo "You typed: $input"
done
