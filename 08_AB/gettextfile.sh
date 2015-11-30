#!/bin/bash

URL="https://nats-www.informatik.uni-hamburg.de/pub/GWV1314/WebHome/heiseticker.tar.gz"

curl -o heiseticker.tar.gz $URL

tar -xzvf heiseticker.tar.gz

rm -rf heiseticker.tar.gz
mv "heiseticker-text.txt" "ht.txt"

echo "File: ht.txt"
