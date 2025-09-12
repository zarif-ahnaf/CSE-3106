inp=""

while [[ "$inp" != "exit" ]]; do
    read -p "Enter a variable" inp
    echo "You have inputted: $inp"
done
