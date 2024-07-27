import random
import time
from web3 import Web3
import config
from modules.color_utils import color_error, color_info, color_success, color_warning, color_reset  # Import color variables

PROXY_CONTRACT_ADDRESS = '0x032139f44650481f4d6000c078820B8E734bF253'
IMPLEMENTATION_CONTRACT_ADDRESS = '0x1a29c466817408768c2D21708cF9041A971d9A78'

PROXY_ABI = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "implementation",
                "type": "address"
            },
            {
                "internalType": "bytes",
                "name": "_data",
                "type": "bytes"
            }
        ],
        "stateMutability": "payable",
        "type": "constructor"
    },
    {
        "stateMutability": "payable",
        "type": "fallback"
    }
]

IMPLEMENTATION_ABI = [
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "pairIndex",
                "type": "uint256"
            },
            {
                "internalType": "bool",
                "name": "isLong",
                "type": "bool"
            }
        ],
        "name": "predictPriceMovement",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

def create_web3_instance(rpc_url, proxy=None):
    return Web3(Web3.HTTPProvider(rpc_url, request_kwargs={"proxies": proxy} if proxy else {}))

def send_transaction(web3, transaction, private_key):
    try:
        signed_tx = web3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        # print(f"{color_success}Transaction successful with hash: {tx_hash.hex()}")
        return receipt
    except Exception as e:
        print(f"{color_error}Error sending transaction: {e}")
        return None

def predict_price_movement(private_key, proxy=None):
    rpc_url = 'https://testnet-rpc.plumenetwork.xyz/http'
    web3 = create_web3_instance(rpc_url, proxy)
    proxy_contract = web3.eth.contract(address=PROXY_CONTRACT_ADDRESS, abi=PROXY_ABI)
    implementation_contract = web3.eth.contract(address=IMPLEMENTATION_CONTRACT_ADDRESS, abi=IMPLEMENTATION_ABI)
    account = web3.eth.account.from_key(private_key)
    
    receipts = []

    for pair_index in range(6):
        is_long = random.choice([True, False])
        data = implementation_contract.encodeABI(fn_name="predictPriceMovement", args=[pair_index, is_long])
        
        tx = {
            'to': PROXY_CONTRACT_ADDRESS,
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'data': data,
            'gas': 500000,
            'gasPrice': web3.to_wei('3', 'gwei')
        }
        
        # print(f"{color_info}Sending transaction for pair_index {pair_index} with is_long={is_long}")
        receipt = send_transaction(web3, tx, private_key)
        # if receipt:
        #     print(f"{color_success}Transaction for pair_index {pair_index} succeeded")
        # else:
        #     print(f"{color_error}Transaction for pair_index {pair_index} failed")
        receipts.append(receipt)
        time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    
    return receipts