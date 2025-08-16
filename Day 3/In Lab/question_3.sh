sum=0

for num in {1..100};do
    sum=$((sum + num))
done

echo "The sum of numbers from 1 to 100 is: $sum"