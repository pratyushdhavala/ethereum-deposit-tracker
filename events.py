from web3 import Web3


def fetch_deposits_from_receipt(w3, contract, tx_hash):
    try:

        receipt = w3.eth.get_transaction_receipt(tx_hash)
        events = contract.events.DepositEvent().processReceipt(receipt)
        deposits = []


        for event in events:

            deposit = {
                "pubkey": event['args']['pubkey'].hex(),
                "withdrawal_credentials": event['args']['withdrawal_credentials'].hex(),
                "amount": int.from_bytes(event['args']['amount'], byteorder='big'),
                "signature": event['args']['signature'].hex(),
                "index": int.from_bytes(event['args']['index'], byteorder='big')
            }


            deposits.append(deposit)

        return deposits

    except Exception as e:

        print(f"Error fetching deposits from receipt: {e}")
        return None