#!/bin/bash
fact=1

read -p "Enter a number: " num1

while ((num1>0));do
    fact=$((fact * num1))
    num1=$((num1 - 1))
done

echo "Factorial of the number is: $fact"