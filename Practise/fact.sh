read -p "Enter a number: " num1;

fact=1;
i=$num1;

while [ $i -gt 1 ]; do
   fact=$((fact * i))
   i=$((i - 1))
done

echo "Factorial of $n is $fact"
