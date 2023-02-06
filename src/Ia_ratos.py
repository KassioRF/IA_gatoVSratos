

"""-----------------------------------------------------------------------------
 Classe IA_Ratos
 Controla os ratos no tabuleiro
-----------------------------------------------------------------------------"""
from .constants import MIN, MAX, COLUNAS, LINHAS
from .regras import *
from .arvore_jogo import No, PilhaFronteira
from .util import print_celulas

from .jogadores import Gato, Ratos
from .tabuleiro import Tabuleiro

import copy


from random import randint

import time 

# import sys
# print(sys.getrecursionlimit())
# sys.setrecursionlimit(12000)

class MinMax():
  
  """
  Verifica se o estado s é terminal
  """
  def teste_terminal(estado):
    # se estado == terminal retorna true
    pass

  """
  Calcula a utilidade do estado s para o jogador j
  """
  def utilidade(estado, jogador):
    # como obter a utilidade ?
    # estará contida no nó
    pass





class Ia_Ratos():

  # teste
  profundidade = 0
  max_profundidade = 15000
  # rato escolhido para o movimento
  escolhido = 0

  time = 0

  def __init__(self, ratos, gato, tabuleiro):
    self.ratos = ratos
    self.gato = gato
    self.tabuleiro = tabuleiro

  # ------------------------------------------------------------------
  # Verifica se o gato está na diagonal inferior esquerda ou direita
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
    gatoy = self.gato.pos[0]

    # conversão da letra da coluna para o índice respectivo da letra
    gatox = self.tabuleiro.Cols.index(self.gato.pos[1])
    ratox = self.tabuleiro.Cols.index(self.ratos.pos[idx][1])

    # se gato nao está 1 linha abaixo a captura já é invalida
    if gatoy == ratoy  - 1:
      # Caso 1:
      if gatox  == ratox - 1:
        # print("caso1")

        y, x = self.ratos.pos[idx]
        y = y - 1      
        x = self.tabuleiro.Cols[ratox - 1] 
        return y, x
    
      # Caso 2:
      elif gatox == ratox + 1 :
        # print("caso2")
        
        y, x = self.ratos.pos[idx]
        y = y - 1
        x = self.tabuleiro.Cols[ratox + 1]
        return y, x

    return [ -1, -1 ]


  # ------------------------------------
  # APENAS PARA TESTE!
  # BOT "FRACO" NAO USA MINMAX
  # Escolhe o rato De forma sequencial 
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
      

  
  # MINIMAX V1
  #-----------------------------------------------------------------------------
  # Retorna ações possíveis para o gato
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
      # else:
      #   print(' y - 2')


    # Caso 2: capturar -> ( y - 1, x - 1 )  ou ( y - 1, x + 1) 
    yy, xx =  self.movimento_captura(idx)
    if (yy, xx) != (-1, -1):
      # captura válida
      valida_yx = valida_movimento_ratos( rato, yy, xx, 
                                      estado.celulas, estado.rodada_inicial )
      if valida_yx:
        acoes.append( (idx, valida_yx[0], valida_yx[1]) )
      # else:
      #   print('captura')

    
    #BUG esta comendo mesmo com obstaculo
    # Caso 3: mover -> (y - 1, x) se nao existe obstáculo
    valida_yx = valida_movimento_ratos( rato, y, x, 
                                      estado.celulas, estado.rodada_inicial )
    if valida_yx:
      acoes.append( (idx, valida_yx[0], valida_yx[1]) )
    # else:
    #   print('normal')
    


    return acoes



  """---------------------------------------------------------------------------
  #########################        MINMAX       ################################
  
  Efetua a recursão descendo até as folhas da árvore de jogo
  
  :return: ação com a melhor utilidade
  (com openente jogando para minimizar a utilidade)
  ---------------------------------------------------------------------------"""
  
  #-----------------------------------------------------
  # Cria uma nova instância de estado a partir do atual
  #-----------------------------------------------------
  # MOVER ESTA FUNCAO PARA UTILS ?
  def get_estado(self, _estado):
    
    gatopos = (y, x) = _estado.gato.pos    
    ratospos = [ (ry, rx) for (ry, rx) in _estado.ratos.pos ]
    # ratospos = copy.deepcopy(_estado.ratos.pos)

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
  
  #-----------------------------------------------------
  # obtém o estado(s) retornado a partir de uma acao(a)
  #-----------------------------------------------------
  def resultado(self, s, acao):
    estado = self.get_estado(s)

    # print(acao)
    if estado.vitoria():
      return s


    if estado.jogador == MAX:
      idx, y, x = acao
      estado.mover_rato(estado.ratos, idx, y, x)

    elif estado.jogador == MIN:
      y, x = acao
      estado.mover_gato(estado.gato, y, x)

      # print_celulas(estado.celulas)

    return estado

  #-----------------------------------------------------
  # Cria uma nova instância de estado a partir do atual
  #-----------------------------------------------------
  
  def minimax(self):
    # estado inicial
    e_inicial = self.get_estado(self.tabuleiro)
    
    # no_raiz = No(pai=None, estado=e_inicial, jogador=e_inicial.jogador, 
    #         utilidade=float('inf'), nivel=0)
    
    # fronteira = PilhaFronteira()
    # fronteira.add(no_raiz)


    # obtém ações disponíveis para cada o ratos do tabuleiro
    acoes = [] 
    for idx in range(e_inicial.ratos.n):      
      acoes += self.acoes_rato(e_inicial, idx)
    
    # quando nao existem acoes possiveis e ainda nao é condição de vitoria
    # quer dizer que existe 1 rato no tabuleiro e ele está bloqueado pelo gato
    if not acoes:
      return -1, -1, -1

    # no = fronteira.remove()
    self.time = time.time()

    #teste
    # e_inicial.rodada_inicial = False
    melhor_utld = [ i for i in range(len(acoes))]


    self.profundidade = 0
    alpha, beta = float('-inf'), float('inf')
    for i in range(len(acoes)):
      # print(acao)
      estado_suc = self.resultado(e_inicial, acoes[i])
      
      estado_suc.rodada_inicial = False
      
      melhor_utld[i] = self.valor_min(estado_suc, alpha, beta, 0)

    
    
    idx = randint(0, len(acoes) - 1)
    melhor = melhor_utld[idx]
    
    # se todas as jogadas pros ratos possuem a mesma utilidade 
    # escolhe um aleatorio
    
    utlds_iguais = all(ut == melhor_utld[0] for ut in melhor_utld)    
    if not utlds_iguais:   
      melhor = max(melhor_utld)          
      idx = melhor_utld.index(melhor)
    
    
    # Em desenvolvimento.....
    print(acoes, melhor, (time.time() - self.time))
    return acoes[idx]

  
  def heuristica(self, s):
    vantagem = 0

    desvantagem = 0

    # vantagem
    # ratos vizinhos em diagonal
    # 
    for idx in range(1, s.ratos.n):
      iy, ix = s.ratos.pos[idx - 1]
      jy, jx = s.ratos.pos[idx]

      if iy == jy - 1 or iy == jy + 1:
        ixx = s.Cols.index(ix)
        jxx = s.Cols.index(jx)
        if ixx == jxx - 1 or ixx == jxx + 1:
          # vantagem += 1 * .25
          vantagem += 1 * (6 - iy)/10
        elif ixx == jxx:
          vantagem += .1 * (6 - iy)/10
      

    # desvantagem
    # qtd ratos com x == gx ou y == gy
    # se verdadeiro dizer que o rato está 1 jogada de pontuar
    # caso contratio está a 2 jogadas de pontuar

    gy, gx = s.gato.pos
    
    for idx in range(s.ratos.n):
      
      ry, rx = s.ratos.pos[idx]
      
      if gy == ry or gx == rx:
        desvantagem += 1 * (s.ratos.n/10)

      if gy > ry:
        desvantagem += .2

    # ratos em vantagem
    vantagem = s.ratos.n - desvantagem

    evals = vantagem - desvantagem

    return evals


  def avaliacao(self, s):
    
    if s.vitoria(MAX) or s.vitoria(MIN):
      if s.jogador == MAX:
        return s.ratos.n
      
      elif s.jogador == MIN:        
        return 6 - s.ratos.n
    
    else:
      return self.heuristica(s)
    
    # if s.jogador == MAX:
    #   if s.vitoria(MAX):
    #     return s.ratos.n
      
    #   else:
    #     return self.heuristica(s)

    # elif s.jogador == MIN:
    #   if s.vitoria(MIN):
    #     return s.ratos.n * -1
      
    #   else:
    #     return self.heuristica(s)
    
    # else:
    #   return 0
  

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


    # print(nivel)
    # if time.time() - self.time < 2:
    #   # print_celulas(s.celulas)
    #   print(s.vitoria(MAX), s.vitoria(MIN), )

    # else:
    #   print(s.rodada_inicial)
    #   raise SystemExit
    
    # if nivel > 10:
    #   print_celulas(s.celulas)
    #   raise SystemExit
    # print("MIN:")


    return v

  # se MIN acoes pro gato
  def valor_max(self, s, alpha, beta, nivel):
    self.profundidade += 1
    print(self.profundidade)
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
      
      # print("\nMAX:")
      # print(melhor_a, i)
      # print_celulas(s_suc.celulas)
      
      v = max(v, self.valor_min(s_suc, alpha, beta, nivel+1))
      # aplica poda alphabeta
      if v >= beta:
        return v
      
      alpha = max(alpha,v)

      melhor_a[i] = v

    v = max(melhor_a)

    return v
