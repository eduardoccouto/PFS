import os

def limparTela():
    return os.system('cls' if os.name == 'nt' else 'clear')