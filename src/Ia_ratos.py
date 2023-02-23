

import copy
from math import sqrt
from functools import reduce
from random import randint, choice
import time 

from .constants import MIN, MAX, COLUNAS, LINHAS, GATOICON, RATOICON
from .regras import *
from .util import print_celulas

from .jogadores import Gato, Ratos
from .tabuleiro import Tabuleiro


"""-----------------------------------------------------------------------------
 Classe IA_Ratos
  - É o agente que controla os ratos no tabuleiro
  
  - Mantém a referência do estado atual do jogo a partir dos parâmetros
    de inicialização:
      - <class.Tabuleiro>
      - <class.Ratos>
      - <class.Gato>

  - Implementa os métodos para obter as ações "A" disponíveis no estado "s" atual
  - Implementa o método para obter o estado sucessor "s" dada uma ação "a"

-----------------------------------------------------------------------------"""
class Ia_Ratos():

  # teste
  profundidade = 0
  
  max_profundidade = float('inf')
  
  # rato escolhido para o movimento quando não usa MinMax ( testes )
  escolhido = 0 
  
  # controla tempo de execução p algumas rotinas
  time = 0

  def __init__(self, ratos, gato, tabuleiro):
    self.ratos = ratos
    self.gato = gato
    self.tabuleiro = tabuleiro


  """---------------------------------------------------------------------------
  ### Métodos do agente ###
  ---------------------------------------------------------------------------"""

  #-----------------------------------------------------------------------------
  # Cria uma nova instância de estado a partir do atual
  # :returns: <class.Tabuleiro> 
  #   Uma cópia independente do Estado de entrada
  #-----------------------------------------------------------------------------
  def get_estado(self, _estado):
    
    gatopos = (y, x) = _estado.gato.pos    
    ratospos = [ (ry, rx) for (ry, rx) in _estado.ratos.pos ]

    rodada_inicial = _estado.rodada_inicial
    jogador = _estado.jogador # MINIMAX sempre é chamada na vez do rato
        
    # gerar novo gato
    gato = Gato()
    gato.set_pos(gatopos[0], gatopos[1]) 

    # gerar novo ratos
    ratos = Ratos()
    ratos.n = len(ratospos)
    ratos.pos = ratospos
    
    # gerar novo tabuleiro 
    celulas = { (y,x) : None  
      for x in _estado.Cols  
      for y in range(1, 9) }
    
    estado = Tabuleiro(celulas=celulas)
    estado.inicializar(gato=gato, ratos=ratos,
                      rodada_inicial=rodada_inicial, jogador=jogador )

    return estado
  
  #-----------------------------------------------------------------------------
  # Obtém o estado "s" gerado a partir de uma acao "a"
  # :returns: <class.Tabuleiro> 
  #   O Estado sucessor de ACAO(s,a)
  #-----------------------------------------------------------------------------
  def resultado(self, s, acao):
    estado = self.get_estado(s)

    if estado.vitoria():
      return s

    if estado.jogador == MAX:
      idx, y, x = acao
      estado.mover_rato(estado.ratos, idx, y, x)

    elif estado.jogador == MIN:
      y, x = acao
      estado.mover_gato(estado.gato, y, x)

    return estado

  #-----------------------------------------------------------------------------
  # Obtém o conjunto de ações possíveis para o gato
  # :returns: lista:[ tuplas(y,x) ]
  #-----------------------------------------------------------------------------
  def acoes_gato(self, estado):
    if estado.gato.pos == None:
      return [ ]

    y, x = estado.gato.pos
    
    acoes = [ ]

    # Caso 1: movimento na linha
    for yy in range(1, estado.altura ):      
      # ignora a posição atual
      if yy == y:
        continue        
      
      if valida_movimento_gato(estado.gato, yy, x, estado.celulas):
        acoes.append( ( yy, x ) )
    
    # Caso 2: movimento na coluna
    for xx in estado.Cols:
      # ignora a posição atual
      if xx == x:
        continue
      
      if valida_movimento_gato(estado.gato, y, xx, estado.celulas):
        acoes.append( ( y, xx ) )
      
    return acoes
  
  #-----------------------------------------------------------------------------
  # Retorna ações possíveis para os ratos existentes no tabuleiro  
  # :returns: lista:[ tuplas(idx, y, x) ]
  #   Onde idx é o rato selecionado para a ação
  #-----------------------------------------------------------------------------
  def acoes_rato(self, estado):    
    # obtém as ações para 1 rato 
    def acoes_ratoIdx(idx):      
      rato = estado.ratos.pos[idx]
      y, x = rato
      y -= 1

      acoes_i = [ ]

      # Caso 1: mover -> ( y - 2, x) quando é a primeira rodada
      if estado.rodada_inicial:
        yy = y - 1
        valida_yx = valida_movimento_ratos( rato, yy, x, 
                                        estado.celulas, estado.rodada_inicial )
        if valida_yx:
          acoes_i.append( (idx, valida_yx[0], valida_yx[1] ) )
          
          # Caso queira mover sempre y - 2 na primeira rodada:
          # return acoes_i


      # Caso 2: capturar -> ( y - 1, x - 1 )  ou ( y - 1, x + 1) 
      yy, xx =  self.movimento_captura(idx, estado)

      if (yy, xx) != (-1, -1):

        # captura válida
        valida_yx = valida_movimento_ratos( rato, yy, xx, 
                                        estado.celulas, estado.rodada_inicial )
      
        if valida_yx:    
          acoes_i.append( (idx, valida_yx[0], valida_yx[1]) )
          # Retorna apenas o mov de captura
          acoes_i = [ (idx, valida_yx[0], valida_yx[1]) ]
          return acoes_i

      # Caso 3: mover -> (y - 1, x) se nao existe obstáculo
      valida_yx = valida_movimento_ratos( rato, y, x, 
                                        estado.celulas, estado.rodada_inicial )

      if valida_yx:
        acoes_i.append( (idx, valida_yx[0], valida_yx[1]) )

      return acoes_i
    
    
    # acoes disponíveis p/ todos os ratos
    acoes = [ ]

    ratos = estado.ratos.pos

    for idx in range(estado.ratos.n):
      acoes += acoes_ratoIdx(idx)

    return acoes


  """---------------------------------------------------------------------------
  ### Métodos auxiliares ###
  ---------------------------------------------------------------------------"""

  # ----------------------------------------------------------------------------
  # Retorna um movimento que captura o gato, quando possível para o rato idx.
  #
  # :param: <idx>  id do rato no tabuleiro
  #
  # :return: (y,x) :: posição de captura
  # ----------------------------------------------------------------------------
  def movimento_captura(self, idx, estado):
    
    ratoy = estado.ratos.pos[idx][0]
    gatoy = estado.gato.pos[0]

    # conversão da letra da coluna para o índice respectivo da letra
    gatox = COLUNAS.index(estado.gato.pos[1])
    ratox = COLUNAS.index(estado.ratos.pos[idx][1])

    # se gato nao está 1 linha abaixo a captura já é invalida
    if gatoy == ratoy  - 1:
  
      # Caso 1: gato.pos( y-1, x-1 )
      if gatox  == ratox - 1:        
        y, x = estado.ratos.pos[idx]
        y = y - 1
        x = COLUNAS[ratox - 1] 
        
        return y, x
    
      # Caso 2: gato.pos( y-1, x+1 )
      elif gatox == ratox + 1 :
        y, x = estado.ratos.pos[idx]        
        y = y - 1        
        x = COLUNAS[ratox + 1]
        
        return y, x

    # sem captura viável
    return [ -1, -1 ]


  # ----------------------------------------------------------------------------
  # APENAS PARA TESTE!
  # BOT "FRACO" NAO USA MINMAX
  # Escolhe o rato De forma sequencial 
  # Caso 1: Existe movimento de captura ( MAIOR PRIORIDADE )
  # Caso 2: Primeiro movimento do jogo, entao permite mover ate 2 casas
  # Caso 3: movimenta 1 casa para frente
  #
  # :return: (idx do rato, linha, coluna)
  # ----------------------------------------------------------------------------
  def escolhe_rato(self):
    
    # teste captura (Caso 1)
    for idx in range(self.ratos.n):
      y, x =  self.movimento_captura(idx)
      # print(y,x)
      if (y,x) != (-1,-1):
        # encontrou uma captura!
        return idx, y, x

        
    # o id do escolhido
    idx = self.escolhido % self.ratos.n    
    
    # atualiza a próxima escolha
    self.escolhido += 1

    # atribui o movimento
    y, x = self.ratos.pos[idx]

    # Caso 2:
    if self.tabuleiro.rodada_inicial:
      y = y - 2
      
      return idx, y, x
    
    # Caso 3:
    # Obs: Se houver somente 1 rato no tabuleiro e, 
    # um gato estiver em (y - 1, x), o rato passa a vez
    y = y - 1
    if self.ratos.n == 1 and self.gato.pos == (y,x):      
      return -1, -1, -1
    
    elif self.gato.pos == (y,x):
      return self.escolhe_rato()

    return idx, y, x
      

