from tracker import track_deposits, track_real_time_blocks, close_tracker
from database import connect_to_db, close_db_connection
from web3 import Web3
from config import INFURA_URL


w3 = Web3(Web3.HTTPProvider(INFURA_URL))


def check_connection():
    if w3.is_connected():
        print("Connected to Ethereum via Infura.")
    else:
        raise Exception("Failed to connect to Ethereum network via Infura.")


def main():

    check_connection()


    mode = input("Enter 'real-time' to track in real time or 'range' to track a block range: ").strip().lower()

    if mode == 'real-time':
        print("Tracking deposits in real-time...")
        track_real_time_blocks()
    elif mode == 'range':

        start_block = int(input("Enter the starting block number: "))
        end_block = int(input("Enter the ending block number (or press Enter to track up to the latest block): ") or None)
        print(f"Tracking deposits from block {start_block} to {end_block or 'latest'}...")
        track_deposits(start_block=start_block, end_block=end_block)
    else:
        print("Invalid option. Please enter 'real-time' or 'range'.")


    close_tracker()

if __name__ == "__main__":
    main()