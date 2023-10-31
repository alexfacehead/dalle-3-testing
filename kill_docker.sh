#!/bin/bash

# Get a list of PIDs related to Docker
PIDS=$(ps -e | grep docker | grep -Eo '\b[0-9]{4,8}\b')

# If there are no PIDs found, print a message and exit
if [ -z "$PIDS" ]; then
    echo "No Docker-related processes found."
    exit 0
fi

# Otherwise, iterate over each PID and kill it
for PID in $PIDS; do
    echo "Killing process with PID: $PID"
    sudo kill $PID
done

echo "All Docker-related processes have been killed."
