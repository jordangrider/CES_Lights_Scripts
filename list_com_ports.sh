#!/bin/bash

# List all devices in /dev/ and filter out serial ports
ports=$(ls /dev/ | grep -E '^ttyACM')

# Iterate through each port and gather information
for port in $ports; do
    echo "Port: /dev/$port"
    info=$(udevadm info --query=all --name=/dev/$port)

    # Print information for the port
    echo "$info"

    # Add a separator for better readability
    echo "----------------------------------------"
done