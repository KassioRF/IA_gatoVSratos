
import platform
import time
from os import system

"""-----------------------------------------------------------------------------
Limpa o console 
----------------------------------------------------------------------------"""
def limpa_console():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


"""-----------------------------------------------------------------------------
Printa msgs de aviso para o jogador
----------------------------------------------------------------------------"""
def alerta_jogador(msg):
    print(f"\n\t{msg}\n")