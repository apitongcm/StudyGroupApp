#! /bin/bash

TARGET_URL="http://127.0.0.1:8000/login/"
DUMMY_USERNAME="dummy"
DICTIONARY=password.txt
COOKIE=cookies.txt

echo "Start of Testing"
TOKEN=$(curl -s -i -b $COOKIE $TARGET_URL | grep -oP 'name="csrfmiddlewaretoken" value="\K[^"]+')

for pw in $(cat $DICTIONARY); do
   echo "Attempt using password: $pw"
   response=$(curl -s -X POST -d "username=$DUMMY_USERNAME&password=$pw&csrfmiddlewaretoken=$TOKEN" $TARGET_URL)
   if echo "$response" | grep -q "Tweet"; then 
	echo "[+] Password found: $pw"
	break
   fi
done

echo "Attempt failed. Update password.txt"