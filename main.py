from src.regras import *
from src.util import *
from  src.constants import *



"""-----------------------------------------------------------------------------
 Classe Gato
 Instancia e movimenta o gato
-----------------------------------------------------------------------------"""
class Gato():
  
  icon = "&"
  
  def __init__(self):
    self.pos = ()

  def inicializar(self):
    # Posição inicial para o gato
    self.pos = (1, "D")

  def set_pos(self, y, x):
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
  

  def __init__(self):
    self.pos = [ () for _ in range(self.n) ]
  
  def inicializar(self):
    # posições iniciais para os ratos
    posicoes = [ (7, "A"), (7, "B"), (7, "C"),
                 (7, "F"), (7, "G"), (7, "H") ]

    for i in range(self.n):
      self.pos[i] = posicoes[i]

  def set_pos(self, idx, y, x):
    self.pos[idx] = ( y, x )


"""-----------------------------------------------------------------------------
 Classe Tabuleiro
 Controla a parte Iterativa do jogo
-----------------------------------------------------------------------------"""

class Tabuleiro():
  # Define o tamanho da borda para a linha e coluna de referencia
  borda = 1
  
  def __init__(self, altura=8, largura=8):  
    self.altura = altura + self.borda
    self.largura = largura + self.borda
    # self.tabuleiro = { (y,x) : None  for x in range(largura)  for y in range(altura) }
    self.tabuleiro = { (y,x) : None  
      for x in REFCOL  
      for y in range(1, altura + 1) }


  # ---------------------------------------------------------
  # inicializa com gato e ratos no estado de partida do jogo
  #----------------------------------------------------------
  def inicializar(self, gato, ratos):

    # add pos do gato
    self.tabuleiro[gato.pos] = gato.icon

    # add ratos no mapa
    for idx in range(ratos.n):
      self.tabuleiro[ratos.pos[idx]] = ratos.icon


    # for y,x in self.tabuleiro.keys():
    #   print(f"({y},{x}) {self.tabuleiro[y,x]}")
  

  # ---------------------------------------------------------
  # Executa o movimento para o gato 
  #----------------------------------------------------------
  
  def mover_gato(self, gato, y, x):
    # previne coordenadas invalidas
    if not valida_movimento_gato(self.tabuleiro, gato, y, x):
      # print('falso')
      return False

    # @TODO verifica se é um estado de captura

    # Atualiza a posicao do gato e o tabuleiro
    self.tabuleiro[gato.pos] = None
    gato.set_pos(y,x)
    self.tabuleiro[gato.pos] = gato.icon

    return True
  
  # ---------------------------------------------------------
  # Executa o movimento para um rato
  #----------------------------------------------------------
  def mover_rato(self, ratos, idx, y, x):
    #@ TODO validacao especifica para gatos e ratos
    # utilizar essa funcao valida para validacao do formato
    # funcao especifica para validacao das regras
    # previne coordenadas invalidas
    if not valida_movimento_ratos(self.tabuleiro, ratos.pos[idx], y, x):
      # print('falso')
      return False

    # @TODO verifica se é um estado de captura

    # Atualiza a posicao do rato no tabuleiro
    self.tabuleiro[ratos.pos[idx]] = None
    ratos.set_pos(idx, y, x)
    self.tabuleiro[ratos.pos[idx]] = ratos.icon

    return True
  # ---------------------------------------------
  # Desenhar tabuleiro
  #----------------------------------------------
  def exibir(self):
    # limpa_console()

    celula_vazia = "___|"
    # REFCOL = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    
    # borda superior    
    print("\n")
    line = "  " + "_"*32
    print(line)
    
    # células
    for y in reversed(range(self.altura)):
      line = ""
      for x in range(self.largura):
        # deixa em branco (0,0)                
        if y == 0 and x == 0:
          line += "  "
          continue
        
        # referência visual para as colunas [A,H] 
        elif y == 0 and x > 0:
          line += f" {REFCOL[x - 1]}  "
        
        # referência visual para as linhas: [8,1]
        elif x == 0:
          line += f"{y}|"

        # pos do gato
        elif self.tabuleiro[ y, REFCOL[x - 1] ] != None:
          line += f"_{self.tabuleiro[y, REFCOL[x - 1]]}_|"


        else:
          line += celula_vazia

      print(line)




if __name__ == "__main__":


  
  #----------------------------------------------
  # Inicializa rotinas
  #----------------------------------------------
  
  # jogadores
  gato = Gato()
  ratos = Ratos()

  gato.inicializar()
  ratos.inicializar()
  


  tabuleiro = Tabuleiro()
  
  tabuleiro.inicializar( gato, ratos )
  
  
  #----------------------------------------------
  # Começa o jogo
  #----------------------------------------------
  
  tabuleiro.exibir()


  #----------------------------------------------
  # testar movimento ratos
  #----------------------------------------------
  # if tabuleiro.mover_gato(gato, 8,'D'):
  #   tabuleiro.exibir()
  # else:
  #   print("coordenada invalida gato")

  # if tabuleiro.mover_gato(gato, 8,'G'):
  #   tabuleiro.exibir()
  # else:
  #   print("coordenada invalida gato")



  if tabuleiro.mover_rato(ratos, 2, 5,'C'):
    tabuleiro.exibir()
  else:
    print("coordenada invalida rato")

  RODADAINICIAL = False


  if tabuleiro.mover_rato(ratos, 2, 4,'C'):
    tabuleiro.exibir()
  else:
    print("coordenada invalida rato")


  if tabuleiro.mover_rato(ratos, 2, 3,'C'):
    tabuleiro.exibir()
  else:
    print("coordenada invalida rato")

  if tabuleiro.mover_rato(ratos, 2, 2,'C'):
    tabuleiro.exibir()
  else:
    print("coordenada invalida rato")

  if tabuleiro.mover_rato(ratos, 2, 1,'C'):
    tabuleiro.exibir()
  else:
    print("coordenada invalida rato")
