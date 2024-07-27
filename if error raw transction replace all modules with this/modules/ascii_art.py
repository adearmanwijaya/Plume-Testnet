from termcolor import colored

def display_ascii_art():
    ascii_art = [
        colored("\n█▀▀ █░█ ▄▀█ █░░ █ █▄▄ █ █▀▀", 'red'),
        colored("█▄█ █▀█ █▀█ █▄▄ █ █▄█ █ ██▄", 'yellow'),

        colored("\nPlume Network Testnet\n", 'green')
    ]
    
    for line in ascii_art:
        print(line)