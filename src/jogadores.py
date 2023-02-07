

from .constants import RATOICON, GATOICON

"""--------------------------------------------------------------------------"""
"""--------------------------------------------------------------------------"""
class Gato():  
  icon = GATOICON
  # pos = None

  def __init__(self):
    self.pos = ()

  def inicializar(self):
    # Posição inicial para o gato
    self.pos = (1, "D")

  def set_pos(self, y, x):
    # atualiza posicao atual do gato
    self.pos = ( y, x )


"""--------------------------------------------------------------------------"""
"""--------------------------------------------------------------------------"""
class Ratos():
  
  icon = RATOICON
  n = 6
  # n = 3
  # Lista de 6 tuplas contendo a posição de cada rato
  pos = [] 

  def __init__(self):
    self.pos = [ () for _ in range(self.n) ]
  
  
  # posições iniciais para os ratos
  def inicializar(self):
    posicoes = [ (7, "A"), (7, "B"), (7, "C"),
                 (7, "F"), (7, "G"), (7, "H") ]

    # posicoes = [ (4, "A"), (4, "B"), (4, ""), (4, "H"), ]

    for i in range(self.n):
      self.pos[i] = posicoes[i]

  
  # atualiza posicao atual do rato idx 
  def set_pos(self, idx, y, x):
    self.pos[idx] = ( y, x )

  #---------------------------------------------------------
  # Remover um rato na coordenada (y,x)
  # método invocado no caso de captura válida na vez do gato 
  #---------------------------------------------------------
  def remove(self, y, x):
    idx = self.pos.index((y,x))
    self.pos.pop(idx)
    self.n -= 1
