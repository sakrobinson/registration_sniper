```bash
#!/bin/bash

# Function to check for a hotkey registration and start mining
check_and_start_mining() {
    # Run the 'btcli w overview' command and store the output
    output=$(btcli w overview --subtensor.network local --wallet.name YOUR_WALLET_NAME)

    # Check if 'HOTKEY_NAME' is in the output
    if echo "$output" | grep -q "HOTKEY_NAME_HERE"; then
        echo "Hotkey found, starting mining script..."
        YOUR_PM2_COMMAND_LINE_HERE
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
```