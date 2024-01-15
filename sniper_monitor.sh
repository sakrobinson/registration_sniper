#!/bin/bash

# Prompt the user for their wallet name, hotkey name, and PM2 command line
read -p "Enter your wallet name: " wallet_name
read -p "Enter your hotkey name: " hotkey_name
read -p "Enter your PM2 command line to start mining: " pm2_command_line

# Function to check for a hotkey registration and start mining
check_and_start_mining() {
    # Run the 'btcli w overview' command and store the output
    output=$(btcli w overview --subtensor.network local --wallet.name "$wallet_name")

    # Check if the hotkey name is in the output
    if echo "$output" | grep -q "$hotkey_name"; then
        echo "Hotkey found, starting mining script..."
        # Execute the PM2 command line provided by the user
        eval "$pm2_command_line"
        exit 0  # Exit the script
    else
        echo "Hotkey not found."
    fi
}

# Main loop
while true; do
    check_and_start_mining
    sleep 30m # Wait for 30 minutes before checking again
done
