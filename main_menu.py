
import subprocess
import os
import json
from getpass import getpass

import json
import os

def read_endpoints():
    data_folder = 'data'
    endpoints_file = 'subtensor_endpoints.json'
    endpoints_path = os.path.join(data_folder, endpoints_file)

    if os.path.exists(endpoints_path):
        with open(endpoints_path, 'r') as file:
            return json.load(file)
    else:
        return []

def save_endpoint(endpoint):
    data_folder = 'data'
    endpoints_file = 'subtensor_endpoints.json'
    endpoints_path = os.path.join(data_folder, endpoints_file)

    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    endpoints = read_endpoints()
    endpoints.append(endpoint)
    with open(endpoints_path, 'w') as file:
        json.dump(endpoints, file)

def registration_sniper():
    bt_netuid = input("To which subnet would you like to register?: ")
    registration_fee_threshold = input("Enter the registration fee threshold: ")

    subtensor_choice = input("Local or Remote subtensor? (local/remote): ").lower()
    if subtensor_choice == "remote":
        endpoints = read_endpoints()
        if endpoints:
            print("Saved endpoints:")
            for i, endpoint in enumerate(endpoints, start=1):
                print(f"{i}. {endpoint}")
            print("Choose from selection or enter manually:")
            endpoint_choice = input("Enter your choice: ")

            if endpoint_choice.isdigit() and int(endpoint_choice) <= len(endpoints):
                bt_endpoint = endpoints[int(endpoint_choice) - 1]
            else:
                bt_endpoint = endpoint_choice
                save_choice = input("Would you like to save this new endpoint for later use? (yes/no): ")
                if save_choice.lower() == 'yes':
                    save_endpoint(bt_endpoint)
        else:
            print("Enter subtensor endpoint:")
            bt_endpoint = input("Enter your Bittensor endpoint: ")
            save_choice = input("Would you like to save this new endpoint for later use? (yes/no): ")
            if save_choice.lower() == 'yes':
                save_endpoint(bt_endpoint)
    else:
        bt_endpoint = "ws://127.0.0.1:9944"

    wallets_path = os.path.expanduser('~/.bittensor/wallets/')
    
    try:
        wallet_names = os.listdir(wallets_path)
    except FileNotFoundError:
        print("The wallet directory does not exist.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return
    
    if not wallet_names:
        print("No wallets found in the directory.")
        return
    
    print("Available wallets:")
    for index, wallet_name in enumerate(wallet_names, start=1):
        print(f"{index}. {wallet_name}")
    
    wallet_index = input("Which wallet would you like to use? (Enter number): ")
    try:
        selected_wallet = wallet_names[int(wallet_index) - 1]
    except (ValueError, IndexError):
        print("Invalid selection. Please enter a number corresponding to the wallet.")
        return

    hotkeys_path = os.path.join(wallets_path, selected_wallet, 'hotkeys')
    
    try:
        all_hotkey_names = os.listdir(hotkeys_path)
    except FileNotFoundError:
        print(f"The hotkeys directory for wallet '{selected_wallet}' does not exist.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    subnet_prefix = f"s{bt_netuid}_"
    hotkey_names = [hk for hk in all_hotkey_names if hk.startswith(subnet_prefix)]

    # Sort the hotkeys by the numerical part
    hotkey_names.sort(key=lambda x: int(x.split('_')[1]))

    if not hotkey_names:
        print(f"No hotkeys found for subnet '{bt_netuid}' in the wallet '{selected_wallet}'.")
        return

    print(f"Available hotkeys for subnet '{bt_netuid}' in wallet '{selected_wallet}':")
    for index, hotkey_name in enumerate(hotkey_names, start=1):
        print(f"{index}. {hotkey_name}")
    
    print("Enter hotkey numbers to register (comma-separated, e.g., 1,3,4):")
    hotkey_indices = input().split(',')
    selected_hotkeys = []
    for index in hotkey_indices:
        try:
            selected_hotkey = hotkey_names[int(index.strip()) - 1]
            selected_hotkeys.append(selected_hotkey)
        except (ValueError, IndexError):
            print(f"Invalid selection: {index}. Skipping.")

    if not selected_hotkeys:
        print("No valid hotkeys selected.")
        return

    bt_cold_pw_wallet = getpass("Enter your Bittensor wallet password: ")

    for selected_hotkey in selected_hotkeys:
        sniper_script_path = os.path.join('src', 'sniper.py')
        pm2_name = f"sniper_{selected_hotkey}"

        # Modify the command to specify 'python3' as the interpreter
        command = [
            'pm2', 'start', 'python3', sniper_script_path,
            '--interpreter', 'python3',  # Specifying the interpreter
            '--name', pm2_name,
            '--',
            '--wallet-name', selected_wallet,
            '--hotkey-name', selected_hotkey,
            '--wallet-password', bt_cold_pw_wallet,
            '--subtensor', subtensor_choice,
            '--endpoint', bt_endpoint,
            '--netuid', bt_netuid,
            '--threshold', registration_fee_threshold,
        ]
        subprocess.run(command)
        print(f"Launched {selected_hotkey} in pm2 instance named {pm2_name}.")

    print("All selected hotkeys have been processed.")

# ... (rest of your script)



def auto_miner_launcher():
    # Placeholder for Auto Miner Launcher functionality
    print("Auto Miner Launcher selected.")
    # TODO: Implement Auto Miner Launcher functionality here
    pass

def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Registration Sniper")
        print("2. Auto Miner Launcher")
        print("3. Save Subtensor Endpoint(s)")
        print("4. Exit")
        
        choice = input("Enter the number of your choice: ")
        
        if choice == '1':
            registration_sniper()
        elif choice == '2':
            auto_miner_launcher()
        elif choice == '3':
            new_endpoint = input("Enter the new endpoint URL to save: ")
            save_endpoint(new_endpoint)
        elif choice == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")

# Run the main menu
main_menu()
