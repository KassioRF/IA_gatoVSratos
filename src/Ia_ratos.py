"""-----------------------------------------------------------------------------
 Classe IA_Ratos
 Controla os ratos no tabuleiro
-----------------------------------------------------------------------------"""
from src.jogadores import *
from src.regras import *
from src.util import *
from src.constants import *
from main import Tabuleiro

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
        print('caso1')
        y, x = self.ratos.pos[idx]
        y = y - 1      
        x = Tabuleiro.Cols[ratox - 1] 
        return y, x
    
      # Caso 2:
      elif gatox == ratox + 1 :
        print('caso2')
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
      
  
