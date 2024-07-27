from eth_account import Account

def get_keys_and_proxies(file_path):
    keys_and_proxies = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2:
                private_key = parts[0]
                proxy_details = parts[1].split('@')
                if len(proxy_details) == 2:
                    credentials, ip_port = proxy_details
                    username, password = credentials.split(':')
                    ip, port = ip_port.split(':')
                    keys_and_proxies.append((private_key, username, password, ip, port))
                else:
                    keys_and_proxies.append((private_key,))
            else:
                keys_and_proxies.append((parts[0],))
    return keys_and_proxies
def get_wallet_address(private_key):
    account = Account.from_key(private_key)
    return account.address