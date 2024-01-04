# Bittensor Registration Sniper

This Python script automates the process of registering on the Bittensor network using the btcli. It allows users to choose between local and remote connections and handles the registration process, looping through registration attempts until one is made, adhering to a specified maximum cost.

## Features

- **Network Selection**: Choose between local and remote networks for registration.
- **User-Friendly Inputs**: Easily input details such as `netuid`, `wallet_name`, `hotkey_name`, and the maximum registration cost.
- **Cost Management**: Automatically checks the registration cost against a user-defined maximum.
- **Automatic Retries**: Continuously retries registration in case of too many registrations in the current interval or if the cost exceeds the specified limit.
- **Secure Password Handling**: Uses `getpass` for secure password input without repeated prompts.

## Requirements

- Python 3
- Bittensor
- Local or Remote Subtensor

## Installation

1. Clone the repository or download the script file.
2. Ensure Python 3 is installed on your system.

## Usage

1. Run the script using Python:

   ```bash
   python3 sniper.py
