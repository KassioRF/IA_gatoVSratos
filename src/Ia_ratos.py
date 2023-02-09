

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
  def verifica_capturaR(self, acao, estado):
    idx, y, _x = acao
    x = COLUNAS.index(_x)
    
    gy, gx = estado.gato.pos[0], COLUNAS.index(estado.gato.pos[1])
    
    #se gato nao está 1 linha abaixo a captura já é invalida
    if gy == y - 1:
      # Caso 1: [y-1, x-1]
      if gx  == x - 1:
        return True
    
      # Caso 2: [ y-1, x+1 ]
      elif gx == x + 1 :      
        return True

    # return False

    return False

  def movimento_captura(self, idx, estado):
    
    ratoy = estado.ratos.pos[idx][0]
    gatoy = estado.gato.pos[0]

    # conversão da letra da coluna para o índice respectivo da letra
    gatox = COLUNAS.index(estado.gato.pos[1])
    ratox = COLUNAS.index(estado.ratos.pos[idx][1])

    # se gato nao está 1 linha abaixo a captura já é invalida
    if gatoy == ratoy  - 1:
  
      # Caso 1: [y-1, x-1]
      if gatox  == ratox - 1:        
        y, x = estado.ratos.pos[idx]
        y = y - 1
        x = COLUNAS[ratox - 1] 
        
        return y, x
    
      # Caso 2: [ y-1, x+1 ]
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
      

  """---------------------------------------------------------------------------
  #########################        MINMAX       ################################
  
  Efetua a recursão descendo até as folhas da árvore de jogo
  
  :param: <Bitr> quando True ativa Busca Imperfeita Em Tempo Real

  :return: ação com a melhor utilidade
  (com openente jogando para minimizar a utilidade)
  ---------------------------------------------------------------------------"""
  
  def minimax(self, Bitr=True):
    
    # teste BITR
    # Bitr = False
    if Bitr:
      self.max_profundidade = 220000
      # self.max_profundidade = 75000


    # estado inicial
    e_inicial = self.get_estado(self.tabuleiro)
    
    # obtém ações disponíveis para cada o ratos do tabuleiro
    acoes = [] 
    for idx in range(e_inicial.ratos.n):      
      
      # Quando captura é disponivel p o rato já retorna de uma vez!
      y, x =  self.movimento_captura(idx, e_inicial)
      
      if (y, x) != (-1, -1):
        print((y, x) != (-1, -1), (idx, y, x), e_inicial.gato.pos)
        return (idx, y, x)

      _acao = self.acoes_rato(e_inicial, idx)            
      acoes += _acao
    
    
    # quando nao existem acoes possiveis e ainda nao é condição de vitoria
    # quer dizer que existe 1 rato no tabuleiro e ele está bloqueado pelo gato
    if not acoes:
      return -1, -1, -1

    
    melhor_utld = [ float('-inf') for i in range(len(acoes))]

    self.time = time.time()
    self.profundidade = 0

    alpha, beta = float('-inf'), float('inf')

    # Chama MinMax para cada acao i
    
    # e_inicial.rodada_inicial = False

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
    
    def protegido(ry, _rx, gy, _gx, ratos ):
      # verifica se um rato está protegido ser capturado
      # assumindo que o gato está na mesma linha ou coluna do rato
      gx = COLUNAS.index(_gx)
      rx = COLUNAS.index(_rx)

      for yy, _xx in ratos:
        xx = COLUNAS.index(_xx)

        # Caso 1: gato na mesma coluna do rato
        if gy == ry or gx == rx:
          # Requisito 1: tem 1 rato na linha de cima?
          if ry + 1 == yy:
            # Requisito 2: esse rato está (x-1) ou (x+1) do rato alvo do gato?
            if rx + 1 < LINHAS \
              and (rx + 1 == xx or rx - 1 == xx):
              # protegido!
              return True

        # Caso 3: o gato não alcança o rato diretamente nem por y nem por x.
        else:
          return True

      # se nenhum cenário de proteção for alcançado rato está vunerável
      return False

    # RATOS acompanhados são mais valiosos:
    def valor_dos_ratos(s):
      ratos = s.ratos.pos
      celulas = s.celulas
      v = [ 0 for i in range(s.ratos.n)]
        
      # Um rato acompanhado quer dizer que:
      # i) existe um rato a esquerda com y-1 ou y+1
      # ii) existe um rato a direita com y-1 ou y+1

      for idx in range(s.ratos.n):
        y, _x = ratos[idx]
        x = COLUNAS.index(_x)

        if x - 1 > 0:
          if celulas[ y + 1, COLUNAS[ x - 1 ] ] == RATOICON or \
           celulas[ y - 1, COLUNAS[ x - 1 ] ] == RATOICON:

            v[idx] += .1

          # elif celulas[ y, COLUNAS[ x - 1 ] ] == RATOICON:
          #   v[idx] += .005

        elif x + 1 < LINHAS:
          if celulas[ y + 1, COLUNAS[ x + 1 ] ] == RATOICON \
            or celulas[ y - 1, COLUNAS[ x - 1 ] ] == RATOICON:
              
              v[idx] += .1

          # elif celulas[ y, COLUNAS[ x + 1 ] ] == RATOICON:
          #   v[idx] += .005              


      return v

    """
      1: Características do estado
        
        i) se linha i contém pelo meos i-1 ratos: 100% vitoria
            ( a partir da linha 5 ) assim priozira o movimento 2 casas
            da primeira rodada

        ii) n de movimentos necessários para o gato capturar o rato mais
            perto de y = 1

    """
    
    # qtd de ratos na linha i
    # adiciona um endereço para representar a linha 0 
    rW = valor_dos_ratos(s)

    # print(rW)
    
    # raise SystemExit

    rfi = [0] + [ 0 for i in range(1, LINHAS + 1) ]
    
    # peso de cada linha i
    # adiciona valor para compensar endereço da linha 0
    w = [0] + [ 1/i for i in range( 1, LINHAS + 1 ) ]

    gy, gx = s.gato.pos
    
    for y, x in s.ratos.pos:
      
      # primeiro verifica se o gato pode capturar o rato com 1 jogada
      if valida_movimento_gato( s.gato, y, x, s.celulas, feedback=False ):
      
        # verifica se o rato está protegido por outro rato        
        if protegido( y, x, gy, gx, s.ratos.pos ):
          rfi[y] += 1.5 # vantagem pro rato
        
        else:
          # as condições anteriores até aqui garantem um cenário onde 
          # pode ter uma captura de rato com o gato em y ou em x
          # ou ambos, com 2 ratos no "campo de vista" do gato
          # A questão é: Neste caso qual rato será capturado ?!

          #
          # como identificar que o melhor pro gato é capturar o mais proximo de y = 1?
          # o gato sempre vai priorizar o rato que oferece maior risco, ou seja,
          # o rato com y mais proximo de 1 é um alvo crítico!
          # Como o objetivo do gato é minimizar a vitoria dos ratos
          # este cenário específico deve reduzir a chance de vitória do gato

          rfi[y] -= (abs( y - 1 )/6) * .2

          # => (y) | quanto menor o (y) do rato i menor o a utilidade deste estado


        # se rato desprotegido descarta o movimento
        # else:
        #   rfi[y] -= 1
      # else:
      #   rfi[y] += 1
      

      # Verifica o cenário onde o gato pode caturar o rato !
      # rato captura gato quando gato em -> ( y - 1, x - 1 )  ou ( y - 1, x + 1) 
      # este é o mais valioso para um rato pois ganha o jogo
      # yy, xx =  self.movimento_captura(s.ratos.pos.index((y,x)), s)      
      # if (yy, xx) != (-1, -1):
      #   rfi[y] += 2
      rfi[y] += rW[s.ratos.pos.index((y,x))]



    # retorna o valor ponderado da melhor linha
    idmx = choice_bestMax(rfi)    
    Eval = rfi[idmx] * w[ idmx ]

    # retorna a média ponderada das linhas


    return Eval


    


  
  
  ### Evals = (s.ratos.n) * 1/dist_y1
  #=============================================================================
  #=============================================================================

  def avaliacao(self, s):    
      if s.vitoria(MAX):
        # print("VITORIA")
        return  MAX

      elif s.vitoria(MIN):
        # print("DERROTA")
        return  MIN

      # else:
      #   return 0
            
      else:
        return self.heuristica(s)

  # COM ALPHA BETA
  # se MAX acoes do rato
  def valor_min(self, s, alpha, beta, nivel):
    self.profundidade += 1
    s.jogador = MIN
    

    if s.vitoria(MIN) or s.vitoria(MAX) \
     or self.profundidade > self.max_profundidade:
      
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


    if s.vitoria(MIN) or s.vitoria(MAX) \
     or self.profundidade > self.max_profundidade \
       or len(acoes) < 1:
      
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
        return acoes


    # Caso 2: capturar -> ( y - 1, x - 1 )  ou ( y - 1, x + 1) 
    yy, xx =  self.movimento_captura(idx, estado)

    if (yy, xx) != (-1, -1):

      # captura válida
      valida_yx = valida_movimento_ratos( rato, yy, xx, 
                                      estado.celulas, estado.rodada_inicial )
    
      if valida_yx:    
        acoes.append( (idx, valida_yx[0], valida_yx[1]) )
        # Retorna apenas o mov de captura
        acoes = [ (idx, valida_yx[0], valida_yx[1]) ]
        return acoes

    # Caso 3: mover -> (y - 1, x) se nao existe obstáculo
    valida_yx = valida_movimento_ratos( rato, y, x, 
                                      estado.celulas, estado.rodada_inicial )

    if valida_yx:
      acoes.append( (idx, valida_yx[0], valida_yx[1]) )

    return acoes


