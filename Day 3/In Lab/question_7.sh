#!/bin/bash

read -p "Enter first number: " num1
read -p "Enter second number: " num2
read -p "Enter third number: " num3

if [ "$num1" -ge "$num2" ] && [ "$num1" -ge "$num3" ]; then
    echo "$num1 is the largest."
elif [ "$num2" -ge "$num1" ] && [ "$num2" -ge "$num3" ]; then
    echo "$num2 is the largest."
else
    echo "$num3 is the largest."
fi

# nums=(12 45 7 99 23)
# max=$(printf "%s\n" "${nums[@]}" | sort -n | tail -1)
# echo "Max is $max"