from secrets import token_hex
from web3 import Web3
from decimal import Decimal, ROUND_DOWN
from modules.color_utils import color_error, color_info, color_success, color_warning, color_reset  # Import color variables

PROXY_CONTRACT_ADDRESS = '0xA34420e04DE6B34F8680EE87740B379103DC69f6'
IMPLEMENTATION_CONTRACT_ADDRESS = '0x7b0a6d394bBD09Faee9dD5Ff27407D4158d495D1'
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
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "stake",
        "outputs": [],
        "stateMutability": "nonpayable",
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

def get_token_balance(web3, token_address, wallet_address):
    token_contract = web3.eth.contract(address=token_address, abi=ERC20_ABI)
    return token_contract.functions.balanceOf(wallet_address).call()

def approve_token(private_key, token_address, spender_address, amount, proxy=None):
    web3 = Web3(Web3.HTTPProvider('https://testnet-rpc.plumenetwork.xyz/http', request_kwargs={"proxies": proxy} if proxy else {}))
    account = web3.eth.account.from_key(private_key)
    
    contract = web3.eth.contract(address=token_address, abi=ERC20_ABI)
    
    nonce = web3.eth.get_transaction_count(account.address)
    approval_tx = contract.functions.approve(spender_address, amount).build_transaction({
        'chainId': 161221135,
        'gas': 500000,
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': nonce
    })
    signed_approval_tx = web3.eth.account.sign_transaction(approval_tx, private_key)
    approval_tx_hash = web3.eth.send_raw_transaction(signed_approval_tx.raw_transaction)
    approval_receipt = web3.eth.wait_for_transaction_receipt(approval_tx_hash)
    
    return approval_receipt

def stake_tokens(private_key, token_address, proxy=None):
    web3 = Web3(Web3.HTTPProvider('https://testnet-rpc.plumenetwork.xyz/http', request_kwargs={"proxies": proxy} if proxy else {}))

    proxy_contract = web3.eth.contract(address=PROXY_CONTRACT_ADDRESS, abi=PROXY_ABI)
    implementation_contract = web3.eth.contract(address=IMPLEMENTATION_CONTRACT_ADDRESS, abi=IMPLEMENTATION_ABI)
    account = web3.eth.account.from_key(private_key)
    wallet_address = account.address
    
    balance = get_token_balance(web3, token_address, wallet_address)
    print(f"{color_warning}Balance for wallet {wallet_address[:5]}...{wallet_address[-5:]}: {balance}")

    if balance == 0:
        print(f"{color_error}Stake | Balance Kosong.")
        return None
    
    # rounded_balance = int(balance / 10**18) * 10**18
    # print(f"{color_info}Balance for staking: {rounded_balance}")

    # if rounded_balance != 0:
    #     print(f"{color_error}Stake | Balance Kurang. Wallet: {wallet_address}")
    #     return None
    
    approval_receipt = approve_token(private_key, token_address, PROXY_CONTRACT_ADDRESS, balance, proxy)
    if approval_receipt['status'] != 1:
        print(f"{color_error}Stake | Approval failed. Transaction hash: {approval_receipt['transactionHash'].hex()}")
        return approval_receipt
    
    stake_data = implementation_contract.encodeABI(fn_name="stake", args=[balance])
    
    gas_limit = 700000
    gas_price = web3.to_wei('3', 'gwei')

    tx = {
        'to': PROXY_CONTRACT_ADDRESS,
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'data': stake_data,
        'gas': gas_limit,
        'gasPrice': gas_price
    }
    
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    return receipt