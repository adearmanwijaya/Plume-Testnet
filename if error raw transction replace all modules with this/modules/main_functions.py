
from modules.file_reader import get_wallet_address
from modules.api_interaction import request_faucet
from modules.contract_interaction import interact_with_proxy_contract
from modules.swap_interaction import swap_tokens
from modules.stake_interaction import stake_tokens
from modules.check_in_interaction import check_in
from modules.prediction_interaction import predict_price_movement
import time
import random
import config
from requests.exceptions import ProxyError, ConnectionError
from modules.color_utils import color_error, color_info, color_success, color_warning, color_reset  # Import color variables



def run_faucet_module(private_key, wallet_address, key_and_proxy=None):
    if key_and_proxy and len(key_and_proxy) == 5:
        proxy = {
            'username': key_and_proxy[1],
            'password': key_and_proxy[2],
            'ip': key_and_proxy[3],
            'port': key_and_proxy[4]
        }
        censored_proxy = f"{key_and_proxy[1][:2]}*****{key_and_proxy[1][-3:]}:{key_and_proxy[2][:2]}*****{key_and_proxy[2][-3:]}@{key_and_proxy[3][:1]}***{key_and_proxy[3][-3:]}:{key_and_proxy[4]}"
        print(f"{color_info}Using proxy: {censored_proxy}")  # Debug print
        try:
            salt, signature = request_faucet(wallet_address, proxy, token="ETH")
            receipt = interact_with_proxy_contract(private_key, salt, signature, token="ETH", proxy=proxy)
            print(f"{color_warning}Claim ETH | Wallet: {wallet_address[:5]}...{wallet_address[-5:]}")
            if receipt['status'] == 1:
                print(f"{color_success}Claim ETH | Transaction successful")
            else:
                print(f"{color_error}Claim ETH | Transaction failed")
            time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
            salt, signature = request_faucet(wallet_address, proxy, token="GOON")
            receipt = interact_with_proxy_contract(private_key, salt, signature, token="GOON", proxy=proxy)
            print(f"{color_warning}Claim GOON | Wallet: {wallet_address[:5]}...{wallet_address[-5:]}")
            if receipt['status'] == 1:
                print(f"{color_success}Claim GOON | Transaction successful")
            else:
                print(f"{color_error}Claim GOON | Transaction failed")
        except ProxyError as e:
            print(f"{color_error}ProxyError for wallet {wallet_address[:5]}...{wallet_address[-5:]}: {e}")
        except ConnectionError as e:
            print(f"{color_error}ConnectionError for wallet {wallet_address[:5]}...{wallet_address[-5:]}: {e}")
        except Exception as e:
            print(f"{color_error}Error processing wallet {wallet_address[:5]}...{wallet_address[-5:]}: {e}")
    else:
        print(f"{color_error}No Proxy for wallet: {wallet_address[:5]}...{wallet_address[-5:]}")
        # Handle faucet without proxy
        try:
            salt, signature = request_faucet(wallet_address, None, token="ETH")
            receipt = interact_with_proxy_contract(private_key, salt, signature, token="ETH")
            print(f"{color_warning}Claim ETH | Wallet: {wallet_address[:5]}...{wallet_address[-5:]}")
            if receipt['status'] == 1:
                print(f"{color_success}Claim ETH | Transaction successful")
            else:
                print(f"{color_error}Claim ETH | Transaction failed")
            time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
            salt, signature = request_faucet(wallet_address, None, token="GOON")
            receipt = interact_with_proxy_contract(private_key, salt, signature, token="GOON")
            print(f"{color_warning}Claim GOON | Wallet: {wallet_address[:5]}...{wallet_address[-5:]}")
            if receipt['status'] == 1:
                print(f"{color_success}Claim GOON | Transaction successful")
            else:
                print(f"{color_error}Claim GOON | Transaction failed")
        except Exception as e:
            print(f"{color_error}Error processing wallet {wallet_address}: {e}")



def run_swap_module(private_key, wallet_address, key_and_proxy=None):
    proxy = None
    if key_and_proxy and len(key_and_proxy) == 5:
        proxy = {
            'username': key_and_proxy[1],
            'password': key_and_proxy[2],
            'ip': key_and_proxy[3],
            'port': key_and_proxy[4]
        }
        censored_proxy = f"{key_and_proxy[1][:2]}*****{key_and_proxy[1][-3:]}:{key_and_proxy[2][:2]}*****{key_and_proxy[2][-3:]}@{key_and_proxy[3][:1]}***{key_and_proxy[3][-3:]}:{key_and_proxy[4]}"
        print(f"{color_info}Using proxy: {censored_proxy}")  # Debug print
        
    else:
        print(f"{color_info}No proxy for wallet: {wallet_address[:5]}...{wallet_address[-5:]}")

    receipt = swap_tokens(private_key, proxy=proxy)
    print(f"{color_warning}Swap | Wallet: {wallet_address[:5]}...{wallet_address[-5:]}")
    if receipt:
        if receipt['status'] == 1:
            print(f"{color_success}Swap | Transaction successful")
        else:
            print(f"{color_error}Swap | Transaction failed")
    else:
        print(f"{color_error}Swap | No receipt returned for wallet: {wallet_address[:5]}...{wallet_address[-5:]}")

def run_stake_module(private_key, wallet_address, key_and_proxy=None):
    proxy = None
    if key_and_proxy and len(key_and_proxy) == 5:
        proxy = {
            'username': key_and_proxy[1],
            'password': key_and_proxy[2],
            'ip': key_and_proxy[3],
            'port': key_and_proxy[4]
        }
        censored_proxy = f"{key_and_proxy[1][:2]}*****{key_and_proxy[1][-3:]}:{key_and_proxy[2][:2]}*****{key_and_proxy[2][-3:]}@{key_and_proxy[3][:1]}***{key_and_proxy[3][-3:]}:{key_and_proxy[4]}"
        print(f"{color_info}Using proxy: {censored_proxy}")  # Debug print
    else:
        print(f"{color_info}No proxy for wallet: {wallet_address[:5]}...{wallet_address[-5:]}")

    token_address = '0x5c1409a46cD113b3A667Db6dF0a8D7bE37ed3BB3'  # Адрес токена для стейкинга
    receipt = stake_tokens(private_key, token_address, proxy=proxy)
    print(f"{color_warning}Stake | Wallet: {wallet_address[:5]}...{wallet_address[-5:]}")
    if receipt:
        if receipt['status'] == 1:
            print(f"{color_success}Stake | Transaction successful")
        else:
            print(f"{color_error}Stake | Transaction failed")
    else:
        print(f"{color_error}Stake | Transaction failed")

def run_check_in_module(private_key, wallet_address, key_and_proxy=None):
    proxy = None
    if key_and_proxy and len(key_and_proxy) == 5:
        proxy = {
            'username': key_and_proxy[1],
            'password': key_and_proxy[2],
            'ip': key_and_proxy[3],
            'port': key_and_proxy[4]
        }
        censored_proxy = f"{key_and_proxy[1][:2]}*****{key_and_proxy[1][-3:]}:{key_and_proxy[2][:2]}*****{key_and_proxy[2][-3:]}@{key_and_proxy[3][:1]}***{key_and_proxy[3][-3:]}:{key_and_proxy[4]}"
        print(f"{color_info}Using proxy: {censored_proxy}")  # Debug print
    else:
        print(f"{color_info}No proxy for wallet: {wallet_address[:5]}...{wallet_address[-5:]}")

    receipt = check_in(private_key, proxy=proxy)
    print(f"{color_warning}Check-in | Wallet: {wallet_address[:5]}...{wallet_address[-5:]}")
    if receipt:
        if receipt['status'] == 1:
            print(f"{color_success}Check-in | Transaction successful")
        else:
            print(f"{color_error}Check-in | Transaction failed")
    else:
        print(f"{color_error}Check-in | Transaction failed")

def run_prediction_module(private_key, wallet_address, key_and_proxy=None):
    proxy = None
    if key_and_proxy and len(key_and_proxy) == 5:
        proxy = {
            'username': key_and_proxy[1],
            'password': key_and_proxy[2],
            'ip': key_and_proxy[3],
            'port': key_and_proxy[4]
        }
        censored_proxy = f"{key_and_proxy[1][:2]}*****{key_and_proxy[1][-3:]}:{key_and_proxy[2][:2]}*****{key_and_proxy[2][-3:]}@{key_and_proxy[3][:1]}***{key_and_proxy[3][-3:]}:{key_and_proxy[4]}"
        print(f"{color_info}Using proxy: {censored_proxy}")  # Debug print
    else:
        print(f"{color_info}No proxy for wallet: {wallet_address[:5]}...{wallet_address[-5:]}")

    receipts = predict_price_movement(private_key, proxy=proxy)
    print(f"{color_warning}Prediction | Wallet: {wallet_address[:5]}...{wallet_address[-5:]}")
    for receipt in receipts:
        if receipt:
            # print(f"{color_info}Receipt details: {receipt}")  # Debug print
            if receipt['status'] == 1:
                print(f"{color_success}Prediction | Transaction successful")
            else:
                print(f"{color_error}Prediction | Transaction failed")
        else:
            print(f"{color_error}Prediction | Transaction failed")

def run_all_modules_for_key(private_key, wallet_address, key_and_proxy=None):
    run_faucet_module(private_key, wallet_address, key_and_proxy)
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    run_swap_module(private_key, wallet_address, key_and_proxy)
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    run_stake_module(private_key, wallet_address, key_and_proxy)
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    run_check_in_module(private_key, wallet_address, key_and_proxy)
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    run_prediction_module(private_key, wallet_address, key_and_proxy)

def run_faucet_swap_stake_for_key(private_key, wallet_address, key_and_proxy=None):
    run_faucet_module(private_key, wallet_address, key_and_proxy)
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    run_swap_module(private_key, wallet_address, key_and_proxy)
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    run_stake_module(private_key, wallet_address, key_and_proxy)
    time.sleep(random.randint(config.module_delay_min, config.module_delay_max))
    run_prediction_module(private_key, wallet_address, key_and_proxy)

def execute_module(keys_and_proxies, module_function, include_proxy=False):
    for key_and_proxy in keys_and_proxies:
        private_key = key_and_proxy[0]
        wallet_address = get_wallet_address(private_key)
        try:
            if include_proxy and len(key_and_proxy) > 1:
                module_function(private_key, wallet_address, key_and_proxy)
            else:
                module_function(private_key, wallet_address)
        except Exception as e:
            print(f"Error processing wallet {wallet_address}: {e}")
        time.sleep(random.randint(config.wallet_delay_min, config.wallet_delay_max))