
from src.jogadores import *
from src.regras import *
from src.util import *
from src.constants import *



"""-----------------------------------------------------------------------------
 Classe Tabuleiro
 Controla a parte Iterativa do jogo
-----------------------------------------------------------------------------"""

class Tabuleiro():
  # ATRIBUTOS ESTÁTICOS DO TABULEIRO
  rodada_inicial = True
  
  # Vez do jogador
  jogador = MAX

  # Referencia para as coluas
  Cols = ["A", "B", "C", "D", "E", "F", "G", "H"]

  # Define o tamanho da borda para a linha e coluna de referencia
  borda = 1
  
  def __init__(self, altura=8, largura=8):  
    self.altura = altura + self.borda
    self.largura = largura + self.borda
    # self.tabuleiro = { (y,x) : None  for x in range(largura)  for y in range(altura) }
    self.tabuleiro = { (y,x) : None  
      for x in self.Cols  
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
  

  # ----------------------------------------------------------------------------
  # Verifica se é estado de vitoria
  #-----------------------------------------------------------------------------
  def vitoria(self, rato_idx=None):
    if self.jogador == MAX:
      if rato_idx != None:
        # verifica se o rato chegou na linha 1
        if Ratos.pos[rato_idx][0] == 1:
          return True
        
        if Gato.pos == None:
          return True
    
    if self.jogador == MIN:
      if Ratos.n <= 0:
        return True

    return False

  # ----------------------------------------------------------------------------
  # Verifica se é estado de captura
  # Obs o metodo só é chamado após (y,x) ser validada pelas regras do jogo
  #-----------------------------------------------------------------------------
  def captura(self, y, x):

    # Rato captura um Gato ?
    if self.jogador == MAX:
      if self.tabuleiro[y,x] == Gato.icon:
        return True

    # Gato captura um Rato ?
    elif self.jogador == MIN:
      if self.tabuleiro[y,x] == Ratos.icon:
        return True
  
    
    return False
  
  # ---------------------------------------------------------
  # Executa o movimento para o gato 
  #----------------------------------------------------------

  def mover_gato(self, gato, y, x):
    # previne coordenadas inválidas de acordo com as regras
    valida_yx = valida_movimento_gato(self.tabuleiro, gato, y, x)
    if not valida_yx:
      return False
    
    y,x = valida_yx
    

    # @TODO verifica se é um estado de captura
    if self.captura(y,x):
      Ratos.remove(y, x)
    


    # Atualiza a posicao do gato e o tabuleiro
    self.tabuleiro[gato.pos] = None
    gato.set_pos(y,x)
    self.tabuleiro[gato.pos] = gato.icon

    return True
  
  # ---------------------------------------------------------
  # Executa o movimento para um rato
  #----------------------------------------------------------
  def mover_rato(self, ratos, idx, y, x):
    # previne coordenadas inválidas de acordo com as regras
    # if not valida_movimento_ratos(self.tabuleiro, ratos.pos[idx], y, x):
    #   return False

    x.upper()

    if self.captura(y,x):
      Gato.pos = None

      

    # Atualiza a posicao do rato no tabuleiro
    self.tabuleiro[ratos.pos[idx]] = None
    ratos.set_pos(idx, y, x)
    self.tabuleiro[ratos.pos[idx]] = ratos.icon

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
        elif self.tabuleiro[ y, self.Cols[x - 1] ] != None:
          line += f"_{self.tabuleiro[y, self.Cols[x - 1]]}_|"


        else:
          line += celula_vazia

      print(line)

    # ratos restantes 
    print(f"\t\t\t\t\t {Ratos.icon}: {Ratos.n}")



"""-----------------------------------------------------------------------------
 Classe IA_Ratos
 Controla os ratos no tabuleiro
-----------------------------------------------------------------------------"""
class IA_Ratos():
  escolhido = 0

  def __init__(self, ratos):
    self.ratos = ratos

  # ------------------------------------------------------------------
  # Verifica se o gato esta na diagonal inferior esquerda ou direita
  # em relação a posicão atual do rato idx.
  #
  # a captura é valida se:
  # gato está em:
  # Caso 1: [y-1, x-1]; Caso 2: [ y-1, x+1 ]; para x,y :: [1,...,8]
  #
  # idx: índice do rato contido na lista de posicoes para os ratos
  # ------------------------------------------------------------------
  def movimento_captura(self, idx):
    ratoy = self.ratos.pos[idx][0]
    gatoy = Gato.pos[0]

    # conversao da letra da coluna para o indice respectivo da letra
    gatox = Tabuleiro.Cols.index(Gato.pos[1])
    ratox = Tabuleiro.Cols.index(self.ratos.pos[idx][1])

    # se gato nao está 1 linha abaixo a captura já é invalida
    if gatoy == ratoy  - 1:
      # Caso 1:
      if gatox  == ratox - 1:
        y, x = self.ratos.pos[idx]
        y = y - 1      
        x = Tabuleiro.Cols[ratox - 1] 
        return y, x
    
      # Caso 2:
      elif gatox == ratox + 1 :
        y, x = self.ratos.pos[idx]
        y = y - 1
        x = Tabuleiro.Cols[ratox + 1]
        return y, x

    return [-1,-1]

  # ------------------------------------
  # Escolhe o rato e o movimento a ser realizado
  # Caso 1: Existe movimento de captura ( MAIOR PRIORIDADE )
  # Caso 2: Primeiro movimento do jogo, entao permite mover ate 2 casas
  # Caso 3: movimenta 1 casa para frente
  #
  # @TODO separar o caso 2 em outro metodo ? reduziria o numero de verificaoes?
  #
  # Retorna: (idx do rato, linha, coluna)
  # ------------------------------------
  def escolhe_rato(self):
    
    # teste captura (Caso 1)
    for idx in range(Ratos.n):
      y, x =  self.movimento_captura(idx)
      # encontrou uma captura!
      # print(y,x)
      if (y,x) != (-1,-1):
        return idx, y, x

        
    # o id do escolhido
    idx = self.escolhido % Ratos.n    
    # atualiza a próxima escolha
    self.escolhido += 1

    # atribui o movimento
    y, x = self.ratos.pos[idx]

    # Caso 2:
    if Tabuleiro.rodada_inicial:
      Tabuleiro.rodada_inicial = False
      y = y - 2
      
      return idx, y, x
    
    # Caso 3:
    y = y - 1
    
    return idx, y, x
      
  



"""-----------------------------------------------------------------------------
  Executa o jogo
-----------------------------------------------------------------------------"""
if __name__ == "__main__":  
  #----------------------------------------------
  # Inicializa rotinas
  #----------------------------------------------
  # jogadores
  gato = Gato()
  gato.inicializar()
  
  ratos = Ratos()
  ratos.inicializar()
  bot = IA_Ratos(ratos)

  # tabuleiro
  tabuleiro = Tabuleiro()  
  tabuleiro.inicializar( gato, ratos )
  
  # jogador da vez
  

  #----------------------------------------------
  # Começa o jogo
  #----------------------------------------------
  limpa_console()
  tabuleiro.exibir()

  capturados = 0
  # jogador que comeca
  Tabuleiro.jogador = MAX


  while (True):

    # VEZ DO Rato
    if Tabuleiro.jogador == MAX:
      #@TODO minimax retorna o rato a ser movimentado
      # e as posicoes y, x
      # tipo retorno (idx, y, x)
      
      # escolhe o rato com movimento valido (sem obstaculo)
      invalidos = 0
      while(True):
        idx, y, x = bot.escolhe_rato()
        if valida_movimento_ratos(tabuleiro.tabuleiro, Ratos.pos[idx], y, x):
          break

        invalidos += 1
        if invalidos == 2:
          break
      
      if tabuleiro.mover_rato(ratos, idx, y, x):
        # limpa_console()
        tabuleiro.exibir()
        # Verifica condicao de vitoria apos o ultimo movimento do rato[idx]
        if tabuleiro.vitoria(idx):
          
          print(f"\n\t Você perdeu =\ \n")
          
          break
      
      # else:
      #   print("coordenada invalida rato")


      Tabuleiro.jogador = MIN
      
    
    # VEZ DO GATO
    if Tabuleiro.jogador == MIN:
      y, x = input("\t Linha: "), input("\tColuna: ")
      if tabuleiro.mover_gato(gato, y, x):
        # limpa_console()
        tabuleiro.exibir()
        
        if tabuleiro.vitoria():
          print(f"\n\t Você venceu!\n")
          break
        
        Tabuleiro.jogador = MAX

    # print(f"{gato.pos}.")
    # print(f"{Gato.pos}..")
    # print(f"{ratos.pos}")
    # print(f"{Ratos.pos}")


  
  #----------------------------------------------
  # testar movimento ratos
  #----------------------------------------------
