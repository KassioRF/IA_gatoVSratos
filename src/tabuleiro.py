
"""-----------------------------------------------------------------------------
 Classe Tabuleiro
 Controla a parte Iterativa do jogo
-----------------------------------------------------------------------------"""
from .constants import *
from pprint import pprint

class Tabuleiro():

  # Vez do jogador
  # jogador = MAX

  # Referência para as coluas
  Cols = COLUNAS

  # Define o tamanho da borda para a linha e coluna de referencia
  borda = 1
  
  def __init__(self, altura=8, largura=8, celulas=None):  
    
    self.altura = altura + self.borda
    self.largura = largura + self.borda
    
    # inicia um novo jogo
    if celulas == None:
      self.celulas = { (y,x) : None  
        for x in self.Cols  
        for y in range(1, altura + 1) }

      self.gato = None
      self.ratos = None
    
    # inicia um tabuleiro com jogo em andamento
    # é o caso para os tabuleiros utilizados minmax
    else: 
      self.celulas = celulas


  # def set_celulas(self, celulas):
  #   self.celulas = celulas

  # ---------------------------------------------------------
  # inicializa com gato e ratos no estado inicial do jogo
  #----------------------------------------------------------
  def inicializar(self, gato, ratos, rodada_inicial=True, jogador=MAX):
    
    self.gato = gato
    self.ratos = ratos
    self.rodada_inicial = rodada_inicial
    
    # insere a coordenada do gato na respectiva célula
    self.celulas[self.gato.pos] = self.gato.icon

    # insere as coordenadas dos ratos nas células
    for idx in range(self.ratos.n):
      self.celulas[self.ratos.pos[idx]] = self.ratos.icon

    # jogador da vez
    self.jogador = jogador

  # ----------------------------------------------------------------------------
  # Verifica se é estado de vitória
  #-----------------------------------------------------------------------------
  def vitoria(self, jogador=None):
    if jogador == None:
      jogador = self.jogador

    if jogador == MAX:
      # verifica se o gato foi capturado
      if self.gato.pos == None:
        return True
      # verifica se algum rato chegou na linha 1
      for idx in range(self.ratos.n):
        if self.ratos.pos[idx][0] == 1:
          return True
        
    
    if jogador == MIN:
      if self.ratos.n <= 0:
        return True

    return False

  # ----------------------------------------------------------------------------
  # Verifica se é estado de captura
  #-----------------------------------------------------------------------------
  def captura(self, y, x):

    # Rato captura um Gato ?
    if self.jogador == MAX:
      if self.celulas[y,x] == self.gato.icon:
        return True

    # Gato captura um Rato ?
    elif self.jogador == MIN:
      if self.celulas[y,x] == self.ratos.icon:
        return True
  
    return False
  
  # ---------------------------------------------------------
  # Executa o movimento para o gato 
  # Assumindo y,x validados
  #----------------------------------------------------------
  def mover_gato(self, gato, y, x):
    # Remove o rato(y,x) quando o movimento é de captura
    # print(":::::::::: CAPTURA!!!!")
    if self.captura(y,x):
      self.ratos.remove(y, x)
    
    # Atualiza a posicao do gato e o tabuleiro
    self.celulas[self.gato.pos] = None
    
    self.gato.set_pos(y,x)
    self.celulas[self.gato.pos] = self.gato.icon

    return True
  
  # ---------------------------------------------------------
  # Executa o movimento para um rato
  # Assumindo y,x validados
  #----------------------------------------------------------
  def mover_rato(self, ratos, idx, y, x):

    x.upper()
    # Remove o gato quando o movimento é de captura
    if self.captura(y,x):
      self.gato.pos = None
    
    # Atualiza a posicao do rato no tabuleiro
    self.celulas[self.ratos.pos[idx]] = None
    self.ratos.set_pos(idx, y, x)
    self.celulas[self.ratos.pos[idx]] = self.ratos.icon

    # if RodadaInicial == True:
    #   RodadaInicial = False

    return True
  
  # ---------------------------------------------
  # Desenhar tabuleiro
  #----------------------------------------------
  def exibir(self):

    celula_vazia = "___|"
    
    # self.Cols = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
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
          line += f" {self.Cols[x - 1]}  "
        
        # referência visual para as linhas: [8,1]
        elif x == 0:
          line += f"{y}|"

        # pos do gato
        elif self.celulas[ y, self.Cols[x - 1] ] != None:
          line += f"_{self.celulas[y, self.Cols[x - 1]]}_|"

        else:
          line += celula_vazia

      print(line)

    # ratos restantes 
    print(f"\t\t\t\t\t {self.ratos.icon}: {self.ratos.n}")


