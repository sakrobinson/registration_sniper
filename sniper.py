import bittensor as bt
from time import sleep
import pexpect
import logging
from logging.handlers import RotatingFileHandler
from getpass import getpass

# Set logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler("reg.log", maxBytes=10000000, backupCount=5),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Prompt for configuration parameters
bt_wallet_name = input("Enter your Bittensor wallet name: ")
bt_hotkey_name = input("Enter your Bittensor hotkey name: ")
bt_cold_pw_wallet = getpass("Enter your Bittensor wallet password: ")
subtensor_choice = input("Local or Remote subtensor? (local/remote): ").lower()
if subtensor_choice == "local":
    bt_endpoint = "ws://127.0.0.1:9944"
elif subtensor_choice == "remote":
    bt_endpoint = input("Enter your Bittensor endpoint: ")
else:
    raise ValueError("Invalid choice. Please enter 'local' or 'remote'.")
bt_netuid = input("Enter your Bittensor network UID: ")
registration_fee_threshold = float(input("Enter the registration fee threshold: "))

# Hardcoded wallet path
bt_wallet_path = "~/.bittensor/wallets"

# Constants
SLEEP_TIME_SHORT = 10
SLEEP_TIME_LONG = 20

# Set config
config = bt.config()
config.name = bt_wallet_name
config.hotkey = bt_hotkey_name
config.path = bt_wallet_path  # Use the hardcoded path
config.chain_endpoint = bt_endpoint
config.netuid = bt_netuid
config.network = "local" if subtensor_choice == "local" else "remote"
config.no_prompt = True

# Initialize wallet and subtensor
wallet = bt.wallet(config.name, config.hotkey, config.path)
subtensor = bt.subtensor(config.chain_endpoint)
logger.info(f"Wallet: {wallet}")
logger.info(f"Subtensor: {subtensor}")

# Registration loop
while True:
    try:
        current_cost = subtensor.burn(config.netuid)
        logger.info("Current cost: %s", current_cost.tao)
        if current_cost.tao < registration_fee_threshold:
            logger.info(
                "Current registration fee below threshold. Attempting to register..."
            )

            child = pexpect.spawn(
                "python3",
                [
                    "-c",
                    f"""
import bittensor as bt
config = bt.config()
config.name = "{config.name}"
config.hotkey = "{config.hotkey}"
config.path = "{config.path}"
config.chain_endpoint = "{config.chain_endpoint}"
config.netuid = {config.netuid}
config.no_prompt = {config.no_prompt}
wallet = bt.wallet(config.name, config.hotkey, config.path)
subtensor = bt.subtensor(config.chain_endpoint)
try:
    subtensor.burned_register(netuid=config.netuid, wallet=wallet)
except Exception as e:
    print(f"Failed to register neuron: {{e}}")
                    """,
                ],
            )
            child.expect("Enter password to unlock key:")
            child.sendline(bt_cold_pw_wallet)
            child.expect(pexpect.EOF, timeout=None)
            output = child.before.decode()
            logger.info(output)  # Print the output from the command

            if "Registered." in output:
                logger.info("Neuron registered.")
                break
            else:
                logger.info("Registration unsuccessful. Waiting to repeat....")
                sleep(SLEEP_TIME_LONG)
        else:
            logger.info("Current registration fee above threshold.")
            logger.info("Waiting to repeat...")
            sleep(SLEEP_TIME_SHORT)
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        sleep(SLEEP_TIME_SHORT)
