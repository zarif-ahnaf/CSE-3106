#!/bin/bash

num=(13 15 6 12 9)
max=$(printf "%s\n" "${num[@]}" | sort -n | tail -1)
echo "Max is $max"