"""-----------------------------------------------------------------------------
 Classe Gato
 Instancia e movimenta o gato
-----------------------------------------------------------------------------"""
class Gato():
  
  icon = "&"
  pos = None

  def __init__(self):
    Gato.pos = ()

  def inicializar(self):
    # Posição inicial para o gato
    Gato.pos = (1, "D")

  def set_pos(self, y, x):
    # atualiza posicao atual do gato
    Gato.pos = ( y, x )


"""-----------------------------------------------------------------------------
 Classe Ratos
 Instancia e movimenta os ratos
 
 Obs: 
 attr <self.pos> armazena uma lista de 6 tuplas contendo a posicao de cada rato 
-----------------------------------------------------------------------------"""
class Ratos():
  
  icon = "#"
  n = 6
  pos = []

  def __init__(self):
    Ratos.pos = [ () for _ in range(self.n) ]
  
  def inicializar(self):
    # posições iniciais para os ratos
    posicoes = [ (7, "A"), (7, "B"), (7, "C"),
                 (7, "F"), (7, "G"), (7, "H") ]

    for i in range(self.n):
      Ratos.pos[i] = posicoes[i]

  def set_pos(self, idx, y, x):
    # atualiza posicao atual do rato idx 
    self.pos[idx] = ( y, x )

  # Remover um rato na coordenada (y,x)
  # método invocado nos casos de captura válida na vez do gato 
  @staticmethod
  def remove( y, x):
    idx = Ratos.pos.index((y,x))
    Ratos.pos.pop(idx)
    Ratos.n -= 1
