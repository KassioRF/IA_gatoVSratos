
"""--------------------------------------------------------------------------"""
 # Classe Tabuleiro:
 #
 # Mantém o estado atual do jogo a cada iteração
 #
 # Resonsável por:
 # - efetuar movimentos; (assumindo que já sejam válidos)
 # - efetuar capturas;
 # - verificação do estado terminal
 # 
 # - também desenha o tabuleiro no console
"""--------------------------------------------------------------------------"""

from .constants import *
from pprint import pprint

class Tabuleiro():
  
  Cols = COLUNAS
  # Define o tamanho da borda para a linha e coluna de referencia
  borda = 1

  # armazena o número de rodads ( só pra mostrar ao lado do placar)
  rodadas = 0

  def __init__(self, altura=LINHAS, largura=LINHAS, celulas=None):  
    
    self.altura = altura + self.borda
    self.largura = largura + self.borda
    
    # inicializa as células
    if celulas == None:
      self.celulas = { (y,x) : None  
        for x in self.Cols  
        for y in range(1, altura + 1) }

      self.gato = None
      self.ratos = None
    
    # inicia células com jogo em andamento
    # este é o caso para os tabuleiros utilizados minmax
    else: 
      self.celulas = celulas

  # ----------------------------------------------------------------------------
  # Inicia o jogo
  # posiciona jogadores, e atribui a rodada inicial para os ratos
  #-----------------------------------------------------------------------------
  def inicializar(self, gato, ratos, rodada_inicial=True, jogador=MAX):
    
    self.gato = gato
    self.ratos = ratos
    
    self.jogador = jogador
    self.rodada_inicial = rodada_inicial
    
    # insere o gato na respectiva célula
    self.celulas[self.gato.pos] = self.gato.icon

    # insere os ratos nas células
    for idx in range(self.ratos.n):
      self.celulas[self.ratos.pos[idx]] = self.ratos.icon


  # ----------------------------------------------------------------------------
  # Executa o movimento para o gato 
  # Assumindo y,x validados
  #-----------------------------------------------------------------------------
  def mover_gato(self, gato, y, x):
    # Remove o rato(y,x) quando o movimento é de captura    
    if self.captura(y,x):
      self.ratos.remove(y, x)
    
    # Atualiza a posicao do gato e o tabuleiro
    self.celulas[self.gato.pos] = None
    
    self.gato.set_pos(y,x)
    
    self.celulas[self.gato.pos] = self.gato.icon

    return True
  
  # ----------------------------------------------------------------------------
  # Executa o movimento para um rato
  # Assumindo y,x validados
  #-----------------------------------------------------------------------------
  def mover_rato(self, ratos, idx, y, x):

    # Remove o gato quando o movimento é de captura
    if self.captura(y,x):
      self.gato.pos = None
    
    # Atualiza a posicao do rato no tabuleiro
    self.celulas[self.ratos.pos[idx]] = None

    self.ratos.set_pos(idx, y, x)

    self.celulas[self.ratos.pos[idx]] = self.ratos.icon

    return True
  
  # ----------------------------------------------------------------------------
  # Verifica se é estado de vitória
  # :return: bool
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
      if self.ratos.n == 0:
        return True

    return False

  # ----------------------------------------------------------------------------
  # Verifica se é estado de captura
  # :return: Bool
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
  
  
  # ---------------------------------------------
  # Desenhar tabuleiro
  #----------------------------------------------
  def exibir(self):
    # padrao celula vazia
    celula_vazia = "___|"
    
    # borda superior    
    print("\n")
    line = "  " + "_"*32 + "\t Rodada: " + str(self.rodadas)
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
    print(f"\t\t\t\t\t Placar {self.ratos.icon}: {self.ratos.n}")


