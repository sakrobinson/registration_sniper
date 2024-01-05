import subprocess
import re
from getpass import getpass

def register_on_bittensor():
    network_choice = input("Connect locally or remotely? [local/remote]: ").strip().lower()
    if network_choice == "local":
        command = 'btcli s register --subtensor.network ws://127.0.0.1:9944'
    elif network_choice == "remote":
        remote_address = input("Enter remote address: ")
        command = f'btcli s register --subtensor.network {remote_address}'
    else:
        print("Invalid choice. Exiting.")
        return

    netuid = input("Enter netuid: ")
    wallet_name = input("Enter wallet name: ")
    hotkey_name = input("Enter hotkey name: ")
    max_cost = float(input("Enter maximum registration cost: "))
    password = getpass("Enter password: ")

    while True:
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        process_input = f"{netuid}\n{wallet_name}\n{hotkey_name}\n"
        output, _ = process.communicate(input=process_input.encode())
        output_str = output.decode()

        # Display the output for the user to see what's happening
        print(output_str)

        cost_match = re.search(r"The cost to register by recycle is τ([\d.]+)", output_str)
        if cost_match:
            current_cost = float(cost_match.group(1))
            print(f"The registration cost is: τ{current_cost}")
            if current_cost > max_cost:
                print(f"Current registration cost exceeds maximum allowed. Retrying immediately...")
                continue

        # At this point, we know the cost is within the limit, so proceed with registration.
        confirm_and_password_input = f"y\n{password}\n"
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, _ = process.communicate(input=confirm_and_password_input.encode())
        output_str = output.decode()

        # Display the output after the registration attempt
        print(output_str)

        if "TooManyRegistrationsThisInterval" in output_str or "TooManyRegistrationsThisBlock" in output_str:
            print("Registration failed due to too many registrations. Retrying immediately...")
        elif "Registered" in output_str:
            print("Registration successful.")
            break
        else:
            print("Registration attempt complete.")
            break

if __name__ == "__main__":
    register_on_bittensor()
