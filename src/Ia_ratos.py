

import copy
from math import sqrt
from functools import reduce
from random import randint, choice
import time 
# import sys
# print(sys.getrecursionlimit())
# sys.setrecursionlimit(12000)
from .constants import MIN, MAX, COLUNAS, LINHAS, GATOICON, RATOICON
from .regras import *
from .util import print_celulas

from .jogadores import Gato, Ratos
from .tabuleiro import Tabuleiro


"""-----------------------------------------------------------------------------
 Classe IA_Ratos
  - Controla os ratos no tabuleiro
  - Implementa MinMax com poda alpha-beta para escolher os movimentos


-----------------------------------------------------------------------------"""
class Ia_Ratos():

  # teste
  profundidade = 0
  
  max_profundidade = float('inf')
  # max_profundidade = 5000
  
  # rato escolhido para o movimento quando não usa MinMAX ( testes )
  escolhido = 0 
  
  # controla tempo de execução p algumas rotinas
  time = 0

  def __init__(self, ratos, gato, tabuleiro):
    self.ratos = ratos
    self.gato = gato
    self.tabuleiro = tabuleiro

  
  # ----------------------------------------------------------------------------
  # Verifica se a posição atual permite a captura do gato
  #
  # a captura é valida se:
  # gato está em:
  # Caso 1: [y-1, x-1]; Caso 2: [ y-1, x+1 ]; para x,y :: [1,...,8]
  #
  # idx: índice do rato contido na lista de posicoes para os ratos
  # :return: (y,x) :: posição de captura
  # ----------------------------------------------------------------------------
  def movimento_captura(self, idx):
  
    ratoy = self.ratos.pos[idx][0]
    gatoy = self.gato.pos[0]

    # conversão da letra da coluna para o índice respectivo da letra
    gatox = self.tabuleiro.Cols.index(self.gato.pos[1])
    ratox = self.tabuleiro.Cols.index(self.ratos.pos[idx][1])

    # se gato nao está 1 linha abaixo a captura já é invalida
    if gatoy == ratoy  - 1:
  
      # Caso 1: [y-1, x-1]
      if gatox  == ratox - 1:
        
        y, x = self.ratos.pos[idx]
        y = y - 1

        x = self.tabuleiro.Cols[ratox - 1] 
        
        return y, x
    
      # Caso 2: [ y-1, x+1 ]
      elif gatox == ratox + 1 :

        y, x = self.ratos.pos[idx]        
        y = y - 1
        
        x = self.tabuleiro.Cols[ratox + 1]
        
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
      

  """---------------------------------------------------------------------------
  #########################        MINMAX       ################################
  
  Efetua a recursão descendo até as folhas da árvore de jogo
  
  :param: <Bitr> quando True ativa Busca Imperfeita Em Tempo Real

  :return: ação com a melhor utilidade
  (com openente jogando para minimizar a utilidade)
  ---------------------------------------------------------------------------"""
  
  def minimax(self, Bitr=True):
    
    # teste BITR

    if Bitr:
      self.max_profundidade = 80000


    # estado inicial
    e_inicial = self.get_estado(self.tabuleiro)
    
    # obtém ações disponíveis para cada o ratos do tabuleiro
    acoes = [] 
    for idx in range(e_inicial.ratos.n):      
      acoes += self.acoes_rato(e_inicial, idx)
    
    # quando nao existem acoes possiveis e ainda nao é condição de vitoria
    # quer dizer que existe 1 rato no tabuleiro e ele está bloqueado pelo gato
    if not acoes:
      return -1, -1, -1

    
    melhor_utld = [ float('-inf') for i in range(len(acoes))]

    self.time = time.time()
    self.profundidade = 0

    alpha, beta = float('-inf'), float('inf')

    # Chama MinMax para cada acao i
    for i in range(len(acoes)):
      
      estado_suc = self.resultado(e_inicial, acoes[i])

      estado_suc.rodada_inicial = False
      
      # armazena a utilidade para a acao i        
      melhor_utld[i] = self.valor_min(estado_suc, alpha, beta, 0)

    # pega o índice da melhor ação
    # - choice é utilizado para casos em que há mais de
    #   uma ação com o maior valor da utilidade. Neste caso
    #   seleciona um max aleatório
    idx = choice_bestMax(melhor_utld)
    
    # testes
    print(f"prof: {self.profundidade}")
    print(f"bs({acoes[idx]}, {round(melhor_utld[idx],4)}), t:{round((time.time() - self.time), 4)}")
    
    return acoes[idx]

  
  
  
  #============================================================================= 
  # HEURISTICA
  #=============================================================================
  def heuristica(self, s):
    """    
      @TODO Definir caracteristicas to estado
      
      (1): soma a distancia de cada rato ate o fim
      (2): soa a distancia do gato capturar um rao

    """
    dist_y1 = 0
    dist_gato = 0

    gy, _gx = s.gato.pos
    gx = s.Cols.index(_gx)

    for idx in range(s.ratos.n):
    
      ry, _rx = s.ratos.pos[idx]
      rx = s.Cols.index(_rx)
      
      dist_y1 += sqrt((rx-rx)**2) + ((ry-1)**2)

      if gy == ry or gx == rx:
        # gato tem chance de capturar na proxima
        # definir um valor melhor p essa chance
        dist_gato += 1
      
      else:
        dist_gato += 2

    if s.jogador == MAX:
      Evals = (s.ratos.n) * (1/dist_y1 - 1/dist_gato)
    
    elif s.jogador == MIN:
      Evals = (6 - s.ratos.n) * (1/dist_y1 - 1/dist_gato)

    else:
      Evals = 0

    return Evals
  
  
  ### Evals = (s.ratos.n) * 1/dist_y1
  #=============================================================================
  #=============================================================================


  def avaliacao(self, s):    
      if s.vitoria(MAX) or s.vitoria(MIN):
        if s.jogador == MAX:
          return s.ratos.n

        elif s.jogador == MIN:
          return 6 - s.ratos.n

        else:
          return 0
            
      else:
        return self.heuristica(s)

  # COM ALPHA BETA
  # se MAX acoes do rato
  def valor_min(self, s, alpha, beta, nivel):
    self.profundidade += 1
    s.jogador = MIN
    

    if s.vitoria(MIN) or s.vitoria(MAX) or self.profundidade > self.max_profundidade:
      return self.avaliacao(s)

    acoes = self.acoes_gato(s)

    v = float('inf')

    for acao in acoes:
      s_suc = self.resultado(s, acao)
      v = min(v, self.valor_max(s_suc, alpha, beta, nivel+1))
      # aplica poda alphabeta
      if v <= alpha:
        return v
      
      beta = min(beta,v)

    return v

  # se MIN acoes pro gato
  def valor_max(self, s, alpha, beta, nivel):
    self.profundidade += 1
    
    s.jogador = MAX

    acoes = [ ]
    for idx in range(s.ratos.n):
      acoes += self.acoes_rato(s, idx)


    if s.vitoria(MIN) or s.vitoria(MAX) or \
     self.profundidade > self.max_profundidade or len(acoes) < 1:
      return self.avaliacao(s)

    melhor_a = [ float('-inf') for i in range(len(acoes))]    
    
    v = melhor_a[0]
    

    for i in range(len(acoes)):
      s_suc = self.resultado(s, acoes[i])
      v = max(v, self.valor_min(s_suc, alpha, beta, nivel+1))
      # aplica poda alphabeta
      if v >= beta:
        return v
      
      alpha = max(alpha,v)

      melhor_a[i] = v

    v = max(melhor_a)

    return v

  #-----------------------------------------------------------------------------
  # // fim MinMax
  #-----------------------------------------------------------------------------

  """---------------------------------------------------------------------------
  ################ Métodos auxiliares utilizados por MinMax ####################
  ---------------------------------------------------------------------------"""

  #-----------------------------------------------------------------------------
  # Cria uma nova instância de estado a partir do atual
  # :returns: <class.Tabuleiro> 
  #   Uma cópia independente do Estado de entrada
  #----------------------------------------------------------------------------
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
  # Obtém o estado(s) retornado a partir de uma acao(a)
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
  # Retorna ações possíveis para o rato
  # :returns: lista:[ tuplas(idx, y, x) ]
  #   Onde idx é o rato selecionado paraa a ação
  #-----------------------------------------------------------------------------
  def acoes_rato(self, estado, idx):
    
    rato = estado.ratos.pos[idx]
    y, x = rato
    y -= 1

    acoes = [ ]

    # Caso 1: mover -> ( y - 2, x) quando é a primeira rodada
    if estado.rodada_inicial:
      yy = y - 1
      valida_yx = valida_movimento_ratos( rato, yy, x, 
                                      estado.celulas, estado.rodada_inicial )
      if valida_yx:
        acoes.append( (idx, valida_yx[0], valida_yx[1] ) )
        
        # Caso queira mover sempre y - 2 na primeira rodada:
        # return acoes


    # Caso 2: capturar -> ( y - 1, x - 1 )  ou ( y - 1, x + 1) 
    yy, xx =  self.movimento_captura(idx)

    if (yy, xx) != (-1, -1):

      # captura válida
      valida_yx = valida_movimento_ratos( rato, yy, xx, 
                                      estado.celulas, estado.rodada_inicial )
    
      if valida_yx:    
        acoes.append( (idx, valida_yx[0], valida_yx[1]) )

    # Caso 3: mover -> (y - 1, x) se nao existe obstáculo
    valida_yx = valida_movimento_ratos( rato, y, x, 
                                      estado.celulas, estado.rodada_inicial )

    if valida_yx:
      acoes.append( (idx, valida_yx[0], valida_yx[1]) )

    return acoes


