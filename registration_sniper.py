import subprocess
import re
from getpass import getpass

def register_on_bittensor():
    # Ask the user to choose between local and remote connection
    network_choice = input("Connect locally or remotely? [local/remote]: ").strip().lower()
    if network_choice == "local":
        # Set command for local connection
        command = 'btcli s register --subtensor.network ws://127.0.0.1:9944'
    elif network_choice == "remote":
        # Prompt for remote address and set command for remote connection
        remote_address = input("Enter remote address: ")
        command = f'btcli s register --subtensor.network {remote_address}'
    else:
        # Exit if an invalid choice is made
        print("Invalid choice. Exiting.")
        return

    # User inputs for netuid, wallet name, hotkey name, and max cost
    netuid = input("Enter netuid: ")
    wallet_name = input("Enter wallet name: ")
    hotkey_name = input("Enter hotkey name: ")
    max_cost = float(input("Enter maximum registration cost: "))

    # Securely capture the password
    password = getpass("Enter password: ")

    # Loop for registration attempts
    while True:
        # Start the registration process with the provided command
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # Provide the initial set of inputs to the command
        process_input = f"{netuid}\n{wallet_name}\n{hotkey_name}\n"
        # Execute the command with the inputs and capture the output
        output, _ = process.communicate(input=process_input.encode())
        output_str = output.decode()

        # Extract the registration cost from the output using regex
        cost_match = re.search(r"The cost to register by recycle is τ([\d.]+)", output_str)
        if cost_match:
            # Convert the extracted cost to float
            current_cost = float(cost_match.group(1))
            # Check if the current cost exceeds the maximum allowed cost
            if current_cost > max_cost:
                print(f"Current registration cost ({current_cost}) exceeds maximum allowed ({max_cost}). Retrying immediately...")
                continue  # Retry immediately if the cost is too high

        # Confirm registration and provide password if cost is within limits
        confirm_and_password_process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        confirm_and_password_input = f"{netuid}\n{wallet_name}\n{hotkey_name}\ny\n{password}\n"
        # Execute the confirmation and password step
        output, _ = confirm_and_password_process.communicate(input=confirm_and_password_input.encode())
        output_str = output.decode()

        # Check for specific errors and retry if necessary
        if "TooManyRegistrationsThisInterval" in output_str or "TooManyRegistrationsThisBlock" in output_str:
            print("Registration failed due to too many registrations. Retrying immediately...")
        else:
            # Exit the loop if registration is successful or a different error occurs
            print("Registration attempt complete.")
            break

# Entry point of the script
if __name__ == "__main__":
    register_on_bittensor()
