from web3 import Web3
from web3.middleware import geth_poa_middleware

def interact_with_proxy_contract(private_key, salt, signature, token="ETH", proxy=None):
    web3 = Web3(Web3.HTTPProvider('https://testnet-rpc.plumenetwork.xyz/http', request_kwargs={"proxies": proxy} if proxy else {}))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    implementation_abi = [
        {
            "inputs": [
                {"internalType": "string", "name": "token", "type": "string"},
                {"internalType": "bytes32", "name": "salt", "type": "bytes32"},
                {"internalType": "bytes", "name": "signature", "type": "bytes"}
            ],
            "name": "getToken",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ]

    proxy_abi = [
        {
            "inputs": [
                {"internalType": "address", "name": "implementation", "type": "address"},
                {"internalType": "bytes", "name": "_data", "type": "bytes"}
            ],
            "stateMutability": "payable",
            "type": "constructor"
        },
        {
            "stateMutability": "payable",
            "type": "fallback"
        }
    ]

    proxy_contract_address = '0x075e2D02EBcea5dbcE6b7C9F3D203613c0D5B33B'
    implementation_contract_address = '0xCAE314d2F47De90e3B13b16eeaf121ee48F509FC'
    
    implementation_contract = web3.eth.contract(address=implementation_contract_address, abi=implementation_abi)
    func_data = implementation_contract.encodeABI(fn_name="getToken", args=[token, salt, signature])
    
    proxy_contract = web3.eth.contract(address=proxy_contract_address, abi=proxy_abi)
    
    account = web3.eth.account.from_key(private_key)
    transaction = {
        'to': proxy_contract_address,
        'value': 0,
        'gas': 2000000,
        'gasPrice': web3.to_wei('1', 'gwei'),
        'nonce': web3.eth.get_transaction_count(account.address),
        'data': func_data
    }
    
    signed_tx = web3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    return receipt