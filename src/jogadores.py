"""-----------------------------------------------------------------------------
 Classe Gato
 Instancia e movimenta o gato
-----------------------------------------------------------------------------"""
class Gato():
  
  icon = "&"
  # pos = None

  def __init__(self):
    self.pos = ()

  def inicializar(self):
    # Posição inicial para o gato
    self.pos = (1, "D")

  def set_pos(self, y, x):
    # atualiza posicao atual do gato
    self.pos = ( y, x )


"""-----------------------------------------------------------------------------
 Classe Ratos
 Instancia e movimenta os ratos
 
 Obs: 
 attr <self.pos> armazena uma lista de 6 tuplas contendo a posicao de cada rato 
-----------------------------------------------------------------------------"""
class Ratos():
  
  icon = "#"
  n = 6
  # n = 2
  pos = []

  def __init__(self):
    self.pos = [ () for _ in range(self.n) ]
  
  def inicializar(self):
    # posições iniciais para os ratos
    posicoes = [ (7, "A"), (7, "B"), (7, "C"),
                 (7, "F"), (7, "G"), (7, "H") ]

    # posicoes = [ (4, "A"), (4, "H"), ]

    for i in range(self.n):
      self.pos[i] = posicoes[i]

  def set_pos(self, idx, y, x):
    # atualiza posicao atual do rato idx 
    self.pos[idx] = ( y, x )

  # Remover um rato na coordenada (y,x)
  # método invocado no caso de captura válida na vez do gato 
  def remove(self, y, x):
    idx = self.pos.index((y,x))
    self.pos.pop(idx)
    self.n -= 1
