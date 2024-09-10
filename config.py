from web3 import Web3
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")



ABI = [
    {"inputs":[],"stateMutability":"nonpayable","type":"constructor"},
    {"anonymous":False,"inputs":[
        {"indexed":False,"internalType":"bytes","name":"pubkey","type":"bytes"},
        {"indexed":False,"internalType":"bytes","name":"withdrawal_credentials","type":"bytes"},
        {"indexed":False,"internalType":"bytes","name":"amount","type":"bytes"},
        {"indexed":False,"internalType":"bytes","name":"signature","type":"bytes"},
        {"indexed":False,"internalType":"bytes","name":"index","type":"bytes"}
    ],"name":"DepositEvent","type":"event"},
    {"inputs":[
        {"internalType":"bytes","name":"pubkey","type":"bytes"},
        {"internalType":"bytes","name":"withdrawal_credentials","type":"bytes"},
        {"internalType":"bytes","name":"signature","type":"bytes"},
        {"internalType":"bytes32","name":"deposit_data_root","type":"bytes32"}
    ],"name":"deposit","outputs":[],"stateMutability":"payable","type":"function"},
    {"inputs":[],"name":"get_deposit_count","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"get_deposit_root","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"}
]


CONTRACT_ADDRESS = '0x00000000219ab540356cBB839Cbe05303d7705Fa'


def connect_to_ethereum():
    return Web3(Web3.HTTPProvider(INFURA_URL))