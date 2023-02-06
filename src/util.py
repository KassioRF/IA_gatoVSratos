
import platform
import time
import random
from os import system

"""-----------------------------------------------------------------------------
Limpa o console 
----------------------------------------------------------------------------"""
def limpa_console():
  
  os_name = platform.system().lower()
  
  if "windows" in os_name:
    system("cls")
  
  else:
    system("clear")


"""-----------------------------------------------------------------------------
Printa msgs de aviso para o jogador
----------------------------------------------------------------------------"""
def alerta_jogador(msg, feedback=False):
  if feedback:
    print(f"\n\t{msg}\n")


"""-----------------------------------------------------------------------------
Printa msgs de aviso para o jogador
----------------------------------------------------------------------------"""
def print_celulas(celulas):
  for y in reversed(range(1, 9)):
    print(str( [ celulas[ y, x ] for x in ["A","B","C","D","E","F","G","H"] ]))



"""-----------------------------------------------------------------------------
 Retorna um indice aletório dentre os valores maximos repetidos na lista values
----------------------------------------------------------------------------"""
def choice_bestMax(values):
  idx = 0
  mx = max(values)
  ids_max = []
  
  for i in range(len(values)):
    if values[i] == mx:
      ids_max.append(i)
  
  return random.choice(ids_max)



def choice_besMin(values):
  pass
