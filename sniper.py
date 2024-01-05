import subprocess
import re
from getpass import getpass
import time

def register_on_bittensor():
    network_choice = input("Connect locally or remotely? [local/remote]: ").strip().lower()
    command = 'btcli s register'
    if network_choice == "local":
        command += ' --subtensor.network ws://127.0.0.1:9944'
    elif network_choice == "remote":
        remote_address = input("Enter remote address: ")
        command += f' --subtensor.network {remote_address}'
    else:
        print("Invalid choice. Exiting.")
        return

    netuid = input("Enter netuid: ")
    wallet_name = input("Enter wallet name: ")
    hotkey_name = input("Enter hotkey name: ")
    max_cost = float(input("Enter maximum registration cost: "))
    password = getpass("Enter password: ")

    while True:
        try:
            with subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True) as process:
                for input_value in [netuid, wallet_name, hotkey_name]:
                    process.stdin.write(f"{input_value}\n")
                    process.stdin.flush()
                    time.sleep(0.5)

                process.stdin.write("y\n")
                process.stdin.flush()
                time.sleep(0.5)
                process.stdin.write(f"{password}\n")
                process.stdin.flush()
                process.stdin.close()

                output_str = process.stdout.read()
                error_str = process.stderr.read()

                print(output_str)
                if error_str:
                    print(f"An error occurred: {error_str}")
                    continue

                if "Insufficient balance" in output_str:
                    print("Insufficient balance to register neuron. Retrying with the same inputs...")
                    continue

                if "TooManyRegistrationsThisInterval" in output_str:
                    print("Registration failed due to too many registrations this interval. Retrying...")
                    continue

                if "Registered" in output_str or "success" in output_str.lower():
                    print("Registration successful.")
                    break
                else:
                    print("Registration attempt complete, but the outcome is unclear. Retrying with the same inputs...")
                    continue

        except Exception as e:
            print(f"An exception occurred: {e}")
            continue

if __name__ == "__main__":
    register_on_bittensor()
