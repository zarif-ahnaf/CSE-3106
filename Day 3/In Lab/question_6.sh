#!/bin/bash
read -p "Enter a file name to check: " FILE

if [ -f $FILE ]; then
    echo "File '$FILE' exists."
else
    echo "File '$FILE' does not exist."
fi
