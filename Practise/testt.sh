#!/bin/bash
inp=""
while [[ $inp != "exit" ]]; do 
    echo "Enter something (type 'exit' to quit):"
    read -r inp
    echo "You entered: $inp"
done