#!/bin/bash

# Find the first ttyACM device
port=$(ls /dev/ttyACM* 2>/dev/null | head -n 1)

if [ -z "$port" ]; then
    echo "No ttyACM device found."
    exit 1
fi

echo "Connecting to $port"

# init serial port for USB device
stty -F "$port" 115200 # raw -echo
set -x
# send each line to serial port, check response between each line
cat -v < "$port" &
echo -e "51,1\n" > "$port"
wait
