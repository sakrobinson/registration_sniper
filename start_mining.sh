#!/bin/bash

# Assign command-line arguments to variables
wallet_name=$1
hotkey_name=$2
pm2_command_line=$3

# Function to check for a hotkey registration and start mining
check_and_start_mining() {
   # Run the 'btcli w overview' command and store the output
   output=$(btcli w overview --subtensor.network local --wallet.name "$wallet_name")
   # Check if the hotkey name is in the output
   if echo "$output" | grep -q "$hotkey_name"; then
       echo "Hotkey found, attempting to start mining script..."

       # Check if the PM2 command line is valid and the script exists
       if command -v pm2 >/dev/null 2>&1 && [ -x "$(command -v $(echo $pm2_command_line | awk '{print $1}'))" ]; then
           # Execute the PM2 command line
           eval $pm2_command_line
           echo "Mining script started."
           exit 0  # Exit the script
       else
           # Error message if PM2 is not installed or the script is not found
           echo "Error: PM2 is not installed or the mining script was not found at the provided path."
           exit 1
       fi
   else
       echo "Hotkey not found."
   fi
}

# Main loop
while true; do
   check_and_start_mining
   sleep 30m # Wait for 30 minutes before checking again
done
