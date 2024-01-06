import bittensor as bt
import socket
import re
import time

def get_numeric_value(balance_obj):
    """Extracts numeric value from a Balance object."""
    balance_str = str(balance_obj)
    # Use regular expression to find the first sequence of digits and optional decimal point
    match = re.search(r"\d+(\.\d+)?", balance_str)
    if match:
        return float(match.group(0))
    else:
        raise ValueError("Failed to extract numeric value from balance object")

def register_neuron(network, netuid, wallet_name, hotkey_name, max_cost, timeout=30, retry_delay=30):
    # Initialize subtensor configuration
    config = bt.subtensor.config()
    config.subtensor.chain_endpoint = network

    # Initialize subtensor connection
    try:
        sub = bt.subtensor(config=config)
        print("Connected to subtensor.")
    except Exception as e:
        print(f"Failed to connect to the Subtensor: {e}")
        return

    # Initialize the wallet with the specified hotkey
    wallet_instance = bt.wallet(name=wallet_name, hotkey=hotkey_name)
    print(f"Initializing wallet with name: {wallet_name} and hotkey: {hotkey_name}")

    # Set socket default timeout
    socket.setdefaulttimeout(timeout)

    while True:
        # Check balance and current registration cost
        balance_obj = sub.get_balance(address=wallet_instance.coldkeypub.ss58_address)
        current_recycle_obj = sub.burn(netuid=netuid)

        # Extract numeric values
        balance = get_numeric_value(balance_obj)
        current_recycle = get_numeric_value(current_recycle_obj)

        print(f"Current balance: {balance}")
        print(f"Current registration cost: {current_recycle}")

        # Check if current registration cost exceeds the maximum allowed cost
        if current_recycle > max_cost:
            print(f"Current registration cost {current_recycle} exceeds the maximum allowed {max_cost}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)  # Wait for 30 seconds before retrying
        else:
            # Attempt to register the neuron
            try:
                print("Attempting to register the neuron...")
                success = sub.register(wallet=wallet_instance, netuid=netuid)
                if success:
                    print("Registration successful.")
                    break
                else:
                    print("Registration failed. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
            except Exception as e:
                print(f"An error occurred during registration: {e}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)


# Main execution
connection_type = input("Connect locally or remotely? (local/remote): ").strip().lower()
network = "ws://127.0.0.1:9944" if connection_type == "local" else input("Enter remote address: ").strip()
netuid = int(input("Enter netuid: "))
wallet_name = input("Enter wallet name: ").strip()
hotkey_name = input("Enter hotkey name: ").strip()
max_cost = float(input("Enter maximum registration cost: "))

register_neuron(network, netuid, wallet_name, hotkey_name, max_cost)
