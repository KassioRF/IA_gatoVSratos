

"""-----------------------------------------------------------------------------
   Métodos auxiliáres
-----------------------------------------------------------------------------"""

import platform
import time
import random
from os import system

"""-----------------------------------------------------------------------------
 Limpa o terminal
-----------------------------------------------------------------------------"""
def limpa_console():
  
  os_name = platform.system().lower()
  
  if "windows" in os_name:
    system("cls")
  
  else:
    system("clear")

"""-----------------------------------------------------------------------------
 Printa msg de aviso para o jogador.

 É um método utilizado para retornar feedbacks para o usuário, caso algo dê 
 errado.

  :param <msg>:
-----------------------------------------------------------------------------"""
def alerta_jogador(msg):
  print(f"\n\t{msg}\n")


"""-----------------------------------------------------------------------------
 Printa as células do tabuleiro no terminal.

 *Obs: útil apenas para testes

  :param <celulas> : dícionário com as coordenadas do tabuleiro
-----------------------------------------------------------------------------"""
def print_celulas(celulas):

  print("\n")
  for y in reversed(range(1, 9)):
    print(str([ celulas[ y, x ] for x in [ "A","B","C","D","E","F","G","H" ] ]))


"""-----------------------------------------------------------------------------
Esta função retorna um índice aleatório de um valor máximo repetido em uma lista.
Ela recebe uma lista de números inteiros como entrada e encontra 
o maior valor nessa lista. Em seguida, ela seleciona um índice aleatório dentre
aqueles que têm o mesmo valor máximo. 

O índice selecionado é retornado como um número inteiro.
  
  :param <values>:
  
  :return: Um número inteiro que representa o índice de algum valor máximo 
            contido na lista.

  :example:
    se values contém [0,1,2,3,3,3,4].
    escolhe aleatóriamente entre os índices com valor 3.
-----------------------------------------------------------------------------"""
def choice_bestMax(values):

  idx = 0
  mx = max(values)
  ids_max = []
  
  for i in range(len(values)):

    if values[i] == mx:
      ids_max.append(i)
  
  return random.choice(ids_max)
