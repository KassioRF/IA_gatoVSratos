


"""-----------------------------------------------------------------------------
 Módulo que implementa as classes dos jogodaores.
-----------------------------------------------------------------------------"""

from .constants import RATOICON, GATOICON

"""-----------------------------------------------------------------------------
Representa a instância do gato no jogo.

Params:
  - icon: str - um caractere que representa o gato no tabuleiro.
  - pos: tupla que armazena a posição atual do gato no formato (y, x).

Métodos:
  - inicializar(): atribui a posição inicial do gato no tabuleiro.
  - set_pos(y, x): atualiza a posição do gato para a coordenada (y, x).
-----------------------------------------------------------------------------"""
class Gato():  
  icon = GATOICON

  def __init__(self):
    self.pos = ()

  """ atribui a posição inicial para o gato. """
  def inicializar(self):
    self.pos = (1, "D")

  """ atualiza posição atual do gato. """
  def set_pos(self, y, x):
    self.pos = ( y, x )


"""-----------------------------------------------------------------------------
Classe que representa o grupo de ratos no jogo.

Params:
  - icon: str - um caractere que representa o rato no tabuleiro.
  - n: int - número de ratos que ainda em jogo.
  - pos: list - uma lista de 6 tuplas que armazena a posição de cada rato.

Métodos:

- inicializar(): Atribui posições iniciais para os ratos.

- set_pos(idx, y, x): Atualiza a posição atual do rato de índice 'idx'.

- remove(y, x): Remove o rato na posição (y, x) da lista de posições dos ratos 
                e decrementa o número de ratos restantes.

-----------------------------------------------------------------------------"""
class Ratos():
  
  icon = RATOICON
  n = 6
  # Lista de 6 tuplas contendo a posição de cada rato
  pos = [] 

  def __init__(self):
    self.pos = [ () for _ in range(self.n) ]
  
  
  """ Atribui posições iniciais para os ratos."""
  def inicializar(self):
    posicoes = [ (7, "A"), (7, "B"), (7, "C"),
                 (7, "F"), (7, "G"), (7, "H") ]

    for i in range(self.n):
      self.pos[i] = posicoes[i]

  
  """ atualiza posicao atual do rato idx."""
  def set_pos(self, idx, y, x):
    self.pos[idx] = ( y, x )

  """ --------------------------------------------------------------------------   
   Remove o idx rato na coordenada (y,x) e decrementa o número de ratos restantes.
    
    :param <y>: inteiro que faz referência p/ linha que o rato se encontra.
  
    :param <x>: string que faz referência p/ coluna que o rato se encontra.

    É método invocado no caso de captura válida na vez do gato.
  -------------------------------------------------------------------------- """
  def remove(self, y, x):
    idx = self.pos.index((y,x))
    self.pos.pop(idx)
    self.n -= 1
