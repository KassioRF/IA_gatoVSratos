from src import MIN, MAX, LINHAS, COLUNAS, GATOICON, RATOICON 
from src import choice_bestMax
from src.regras import valida_movimento_gato, verifica_capturaR
from heuristica import heuristica
import time


"""---------------------------------------------------------------------------
#########################        MINMAX       ################################

  Efetua a recursão descendo até as folhas da árvore de jogo ou
  até o limite da profundidade da busca.

  :param: <bot> é o agente responsável pelo controle dos ratos no jogo
  :param: <Bitr> quando True ativa Busca Imperfeita Em Tempo Real

  :return: ação com a melhor utilidade encontrada

---------------------------------------------------------------------------"""
def minimax(bot, Bitr=True):
  
  # teste BITR
  # Bitr = False
  if Bitr:
    bot.profundidade = 0 # contador de profundidade
    # bot.max_profundidade = 50000
    bot.max_profundidade = 150000


  # estado inicial
  e_inicial = bot.get_estado(bot.tabuleiro)
  
  # obtém ações disponíveis para cada rato do tabuleiro
  acoes = bot.acoes_rato(e_inicial)

  # quando nao existem acoes possiveis e ainda nao é condição de vitoria
  # quer dizer que existe 1 rato no tabuleiro e ele está bloqueado pelo gato
  if not acoes:
    return -1, -1, -1

  bot.time = time.time()
  
  alpha, beta = float('-inf'), float('inf')

  melhor_utld = [ float('-inf') for i in range(len(acoes))]
  
  # MinMax p/ avaliar o movimento de cada um dos ratos no tabuleiro
  for i in range(len(acoes)):    
    
    estado_suc = bot.resultado(e_inicial, acoes[i])    
    # Inicia a recursão na árvore do jogo a partir do estado_inicial

    melhor_utld[i] = valor_min(bot, estado_suc, alpha, beta)


  # pega o índice da melhor ação em ações
  # - choice é utilizado para cobrir os casos em que há mais de
  #   uma ação com o maior valor da utilidade. 
  #   Neste caso seleciona um max aleatório.
  idx = choice_bestMax(melhor_utld)
  
  # testes
  print(f"prof: {bot.profundidade}")
  print(f"bs({acoes[idx]}, {round(melhor_utld[idx],4)}), t:{round((time.time() - bot.time), 4)}")
  
  return acoes[idx]


def avaliacao(s):    
  if s.vitoria(MAX):
    return  MAX

  elif s.vitoria(MIN):
    return  MIN 

  else:
    return heuristica(s)

# COM ALPHA BETA
# se MAX acoes do rato
def valor_min(bot, s, alpha, beta):
  
  bot.profundidade += 1
  s.jogador = MIN
  # s.jogador = MAX
  

  if s.vitoria(MIN) or s.vitoria(MAX) \
    or bot.profundidade > bot.max_profundidade:
    
    return avaliacao(s)

  # ações disponíveis p/ o gato no estado s
  acoes = bot.acoes_gato(s)

  v = float('inf')

  for acao in acoes:
    s_suc = bot.resultado(s, acao)
    v = min(v, valor_max(bot, s_suc, alpha, beta))
    
    # aplica poda alphabeta
    if v <= alpha:
      return v
    
    beta = min(beta,v)

  return v

# se MIN acoes pro gato
def valor_max(bot, s, alpha, beta):
  
  bot.profundidade += 1  
  s.jogador = MAX
  # s.jogador = MIN
  s.rodada_inicial = False

  # obtém acções disponíveis p/ os ratos no estado "s"
  acoes = bot.acoes_rato(s)
  
  if s.vitoria(MIN) or s.vitoria(MAX) \
    or bot.profundidade > bot.max_profundidade \
      or len(acoes) < 1:
    
      return avaliacao(s)
    

  # armazena o valor da utilidade das ações p/ cada rato
  melhor_a = [ float('-inf') for i in range(len(acoes))]    
  v = melhor_a[0]
  
  for i in range(len(acoes)):
    s_suc = bot.resultado(s, acoes[i])

    v = max(v, valor_min(bot, s_suc, alpha, beta))
    # aplica poda alphabeta
    if v >= beta:
      return v
    
    alpha = max(alpha,v)
    # melhor ação do rato i
    melhor_a[i] = v

  v = max(melhor_a)

  return v


#-----------------------------------------------------------------------------
# // fim MinMax
#-----------------------------------------------------------------------------
