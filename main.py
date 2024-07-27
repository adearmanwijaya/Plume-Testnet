from modules.file_reader import get_keys_and_proxies
from modules.ascii_art import display_ascii_art
from modules.main_functions import execute_module, run_faucet_module, run_swap_module, run_stake_module, run_check_in_module, run_all_modules_for_key, run_faucet_swap_stake_for_key, run_prediction_module
import random
import config
import time

def main_menu():
    display_ascii_art()
    print("Pilih Menu:")
    print("1. Run all")
    print("2. Faucet > Swap > Stake > Prediction")
    print("3. Faucet")
    print("4. Swap")
    print("5. Stake")
    print("6. Check-in")
    print("7. Prediction")
    print("8. Exit")
    choice = input("Masukan pilihan: ")

    file_path = 'data.txt'  # Updated file path
    keys_and_proxies = get_keys_and_proxies(file_path)
    
    if not keys_and_proxies:
        print("Error: No valid keys and proxies found in file.")
        return

    random.shuffle(keys_and_proxies)

    if choice == '1':
        execute_module(keys_and_proxies, run_all_modules_for_key, include_proxy=True)
    elif choice == '2':
        execute_module(keys_and_proxies, run_faucet_swap_stake_for_key, include_proxy=True)
    elif choice == '3':
        execute_module(keys_and_proxies, run_faucet_module, include_proxy=True)
    elif choice == '4':
        execute_module(keys_and_proxies, run_swap_module, include_proxy=True) 
    elif choice == '5':
        execute_module(keys_and_proxies, run_stake_module, include_proxy=True)
    elif choice == '6':
        execute_module(keys_and_proxies, run_check_in_module, include_proxy=True)
    elif choice == '7':
        execute_module(keys_and_proxies, run_prediction_module, include_proxy=True)
    elif choice == '8':
        print("Exit...")
        return
    else:
        print("Invalid choice. Please try again.")
    
    main_menu()

if __name__ == "__main__":
    main_menu() 