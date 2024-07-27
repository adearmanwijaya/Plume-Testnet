import requests
import json

def request_faucet(wallet_address, proxy, token):
    url = "https://faucet.plumenetwork.xyz/api/faucet"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "walletAddress": wallet_address,
        "token": token
    }
    
    proxies = None
    if proxy:
        if isinstance(proxy, dict) and all(k in proxy for k in ('username', 'password', 'ip', 'port')):
            username = proxy['username']
            password = proxy['password']
            ip = proxy['ip']
            port = proxy['port']
            # print(f"Proxy details - Username: {username}, Password: {password}, IP: {ip}, Port: {port}")
            proxy_url = f"http://{username}:{password}@{ip}:{port}"
            proxies = {"http": proxy_url, "https": proxy_url}
            # print(f"Using proxy: {proxy_url}")  # Log the proxy URL for debugging
        else:
            print(f"Error: Proxy details should contain 'username', 'password', 'ip', and 'port'. Got: {proxy}")
            raise ValueError("Invalid proxy details format")
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), proxies=proxies)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
        if response.status_code == 200 or response.status_code == 202:
            data = response.json()
            return data.get('salt'), data.get('signature')
        else:
            raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")
    except requests.exceptions.ProxyError as e:
        print(f"ProxyError: {e}")
        raise
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        raise