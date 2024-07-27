from web3 import Web3
import time
from modules.color_utils import color_error, color_info, color_success, color_warning, color_reset  # Import color variables

 
SWAP_CONTRACT_ADDRESS = '0x4c722A53Cf9EB5373c655E1dD2dA95AcC10152D1'
PROXY_CONTRACT_ADDRESS = '0x032139f44650481f4d6000c078820B8E734bF253'
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

SWAP_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "base", "type": "address"},
            {"internalType": "address", "name": "quote", "type": "address"},
            {"internalType": "uint256", "name": "poolIdx", "type": "uint256"},
            {"internalType": "bool", "name": "isBuy", "type": "bool"},
            {"internalType": "bool", "name": "inBaseQty", "type": "bool"},
            {"internalType": "uint128", "name": "qty", "type": "uint128"},
            {"internalType": "uint16", "name": "tip", "type": "uint16"},
            {"internalType": "uint128", "name": "limitPrice", "type": "uint128"},
            {"internalType": "uint128", "name": "minOut", "type": "uint128"},
            {"internalType": "uint8", "name": "reserveFlags", "type": "uint8"}
        ],
        "name": "swap",
        "outputs": [
            {"internalType": "int128", "name": "baseFlow", "type": "int128"},
            {"internalType": "int128", "name": "quoteFlow", "type": "int128"}
        ],
        "stateMutability": "payable",
        "type": "function"
    }
]

ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_spender", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"name": "success", "type": "bool"}],
        "type": "function"
    }
]

BASE = Web3.to_checksum_address('0x5c1409a46cd113b3a667db6df0a8d7be37ed3bb3')
QUOTE = Web3.to_checksum_address('0xba22114ec75f0d55c34a5e5a3cf384484ad9e733')
POOL_IDX = 36000
IS_BUY = False
IN_BASE_QTY = False
QTY = 100000000000000000  # Approximate token quantity
TIP = 0
LIMIT_PRICE = 65537
MIN_OUT = 9690103065591420100  # Approximate minimum output quantity (adjusted by 1 zero)
RESERVE_FLAGS = 0

def swap_tokens(private_key, proxy=None):
    web3 = Web3(Web3.HTTPProvider('https://testnet-rpc.plumenetwork.xyz/http', request_kwargs={"proxies": proxy} if proxy else {}))
    account = web3.eth.account.from_key(private_key)
    
    proxy_contract = web3.eth.contract(address=PROXY_CONTRACT_ADDRESS, abi=PROXY_ABI)
    swap_contract = web3.eth.contract(address=SWAP_CONTRACT_ADDRESS, abi=SWAP_ABI)

    def approve_tokens(private_key, token_address, spender_address, amount):
        token_contract = web3.eth.contract(address=token_address, abi=ERC20_ABI)
        nonce = web3.eth.get_transaction_count(account.address)
        approve_tx = token_contract.functions.approve(spender_address, amount).build_transaction({
            'chainId': 161221135,
            'gas': 500000,
            'gasPrice': web3.to_wei('5', 'gwei'),
            'nonce': nonce
        })
        signed_approve_tx = web3.eth.account.sign_transaction(approve_tx, private_key)
        approve_tx_hash = web3.eth.send_raw_transaction(signed_approve_tx.rawTransaction)
        return web3.eth.wait_for_transaction_receipt(approve_tx_hash)

    approve_receipt = approve_tokens(private_key, BASE, SWAP_CONTRACT_ADDRESS, QTY)
    if approve_receipt['status'] != 1:
        print(f"{color_error}Approval failed.")
        return approve_receipt

    time.sleep(20) 
    
    nonce = web3.eth.get_transaction_count(account.address)
    tx = swap_contract.functions.swap(BASE, QUOTE, POOL_IDX, IS_BUY, IN_BASE_QTY, QTY, TIP, LIMIT_PRICE, MIN_OUT, RESERVE_FLAGS).build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gas': 500000,
        'gasPrice': web3.to_wei('5', 'gwei')
    })
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    return receipt if receipt else {'status': 0, 'transactionHash': None}
 
