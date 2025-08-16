#!/bin/bash


read num;

if [ "$num" -gt 0 ]; then 
	echo "The number is larger than 0"
elif [ "$num" -eq 0 ]; then
	echo "The Number is zero"
else 
	echo "The number is smaller than 0"
fi
