from database import connect_to_db, close_db_connection
from events import fetch_deposits_from_receipt
from web3 import Web3
import logging
import time
from config import INFURA_URL, CONTRACT_ADDRESS, ABI


logging.basicConfig(filename='eth_deposit_tracker.log', level=logging.ERROR)


w3 = Web3(Web3.HTTPProvider(INFURA_URL))


contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)


connection, cursor = connect_to_db()

if not connection:
    raise Exception("Failed to connect to the database.")


def fetch_deposit_data(tx_hash):
    try:

        tx = w3.eth.get_transaction(tx_hash)
        receipt = w3.eth.get_transaction_receipt(tx_hash)


        tx_details = {
            "block_number": tx.blockNumber,
            "transaction_hash": tx.hash.hex(),
            "sender_address": tx['from'],
            "receiver_address": tx['to'],
            "value": w3.from_wei(tx['value'], 'ether'),
            "gas_used": receipt.gasUsed,
            "timestamp": w3.eth.get_block(tx.blockNumber)['timestamp']
        }


        deposit_logs = fetch_deposits_from_receipt(w3, contract, tx_hash)

        if deposit_logs:
            tx_details['deposits'] = deposit_logs


            pubkey_list = [deposit['pubkey'] for deposit in deposit_logs]
            withdrawal_credentials_list = [deposit['withdrawal_credentials'] for deposit in deposit_logs]
            amount_list = [deposit['amount'] for deposit in deposit_logs]
            signature_list = [deposit['signature'] for deposit in deposit_logs]
            index_list = [deposit['index'] for deposit in deposit_logs]


            insert_query = """
                INSERT INTO deposits (
                    block_number, transaction_hash, sender_address, receiver_address,
                    value, gas_used, timestamp, pubkey, withdrawal_credentials, amount, signature, deposit_index
                ) VALUES (%s, %s, %s, %s, %s, %s, TO_TIMESTAMP(%s), %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                tx_details['block_number'],
                tx_details['transaction_hash'],
                tx_details['sender_address'],
                tx_details['receiver_address'],
                tx_details['value'],
                tx_details['gas_used'],
                tx_details['timestamp'],
                pubkey_list,
                withdrawal_credentials_list,
                amount_list,
                signature_list,
                index_list
            ))

            connection.commit()

        return tx_details
    except Exception as e:
        print(f"Error fetching transaction data: {e}")
        connection.rollback()
        return None


def track_deposits(start_block=None, end_block=None):
    latest_block = w3.eth.block_number if end_block is None else end_block
    block = start_block if start_block else latest_block - 10

    for block_number in range(block, latest_block + 1):
        print(f"Checking block {block_number}...")
        block_data = w3.eth.get_block(block_number, full_transactions=True)

        for tx in block_data.transactions:
            if tx.to and tx.to.lower() == CONTRACT_ADDRESS.lower():
                deposit_data = fetch_deposit_data(tx.hash)
                if deposit_data:
                    print(f"Deposit found in block {block_number}: {deposit_data}")



def track_real_time_blocks():
    latest_block = w3.eth.block_number

    while True:
        try:
            current_block = w3.eth.block_number

            if current_block > latest_block:
                print(f"New block detected: {current_block}")
                block_data = w3.eth.get_block(current_block, full_transactions=True)

                for tx in block_data.transactions:
                    if tx.to and tx.to.lower() == CONTRACT_ADDRESS.lower():
                        deposit_data = fetch_deposit_data(tx.hash)
                        if deposit_data:
                            print(f"Deposit found in block {current_block}: {deposit_data}")
                            logging.info(f"Deposit found: {deposit_data}")

                latest_block = current_block
            time.sleep(10)
        except Exception as e:
            error_message = f"Error processing block {current_block}: {e}"
            print(error_message)
            logging.error(error_message)
            time.sleep(10)


def close_tracker():
    close_db_connection(connection, cursor)