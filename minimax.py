from src import MIN, MAX, LINHAS, COLUNAS, GATOICON, RATOICON 
from src import choice_bestMax
from src.regras import valida_movimento_gato
from heuristica import heuristica
import time


"""---------------------------------------------------------------------------
#########################        MINMAX       ################################

  Busca o melhor movimento para o turno atual do agente que controla os ratos.
  
  :param <bot>: é o agente responsável por controlar os ratos no jogo.
  :param <Bitr>: quando True ativa Busca Imperfeita Em Tempo Real.

  :return: ação para o rato com a melhor utilidade encontrada.
            tupla (idx, y, x)

-----------------------------------------------------------------------------"""
def minimax(bot, Bitr=True, profundidade=5):
  
  if Bitr:
    # se for com busca imperfeita em tempo real, define a profundidade.
    bot.max_profundidade = profundidade
  
  # ----------------------------------------------------------------------------
  # reune as informações necessárias p/ iniciar a busca a partir do estado atual. 

  # estado atual do jogo. ( class <src.Tabuleiro> )
  e_inicial = bot.get_estado(bot.tabuleiro)
  
  # lista de tuplas com as ações disponíveis p/ cada rato no tabuleiro.
  acoes = bot.acoes_rato(e_inicial)
 
  # Trata o caso de quando existe 1 rato no tabuleiro e ele está bloqueado pelo gato.
  if not acoes:
    return -1, -1, -1

  # Registra o tempo gasto até decidir movimento.
  bot.time = time.time()
  
  # inicializa as variáveis de controle da poda alpha/beta do minmax
  alpha, beta = float('-inf'), float('inf')

  # inicializa a lista que irá armazenar o resultado do algorítmo minmax 
  # para cada ação disponível p/ os ratos no tabuleiro.
  melhor_utld = [ float('-inf') for i in range(len(acoes))]
  
  #-----------------------------------------------------------------------------
  # Para cada ação disponível, inicia a recursão que irá descer até as folhas da árvore 
  # de jogo ou até o limite da profundidade da busca.
  for i in range(len(acoes)):        
        
    # estado sucessor obtido a partir da ação i
    estado_suc = bot.resultado(e_inicial, acoes[i])    

    # resultado minmax p/ ação i
    melhor_utld[i] = valor_min(bot, estado_suc, alpha, beta, n=0)


  # ----------------------------------------------------------------------------
  # recupera a ação encontrada com a utilidade de maior valor.

  # pega o índice da melhor ação em ações
  # - src.util.choice_bestMax() é utilizada para cobrir os casos em que há mais de
  #   uma ação com o maior valor da utilidade.
  #   Neste caso seleciona um max aleatório.
  idx = choice_bestMax(melhor_utld)

  # Mostra no console algumas informações relevantes sobre o resultado do método.
  print(f"Rato({acoes[idx][2]}) movimenta para:{acoes[idx][1:]} \
   com chance de vitória: {round(melhor_utld[idx],4)} \
    | t:{round((time.time() - bot.time), 4)}")
  

  # retorna (idx, y, x)
  return acoes[idx]


"""
Retorna o valor da avaliação para um estado s.

  :param <s>: estado do jogo (class <src.Tabuleiro>).
  
  Se for um estado de vitória p/ MAX retorna 1
  Se for um estado de vitória p/ MIN retorna -1

  Se s não é um estado de vitória, então retorna uma avaliação
  heurística do estado s.
"""
def avaliacao(s):    
  if s.vitoria(MAX):
    return  MAX

  elif s.vitoria(MIN):
    return  MIN 

  else:
    return heuristica(s)

"""
Implementa a função do jogador MIN do algoritmo minmax para determinar 
o valor de um estado s.

  :param <bot>: instância agente que controla os ratos.
  :param <s>: estado atual do jogo.
  :param <alpha>: o valor atual de alpha.
  :param <beta>: o valor atual de beta.
  :param <n>: a profundidade atual da busca.

  :returns: o valor da função de avaliação para o estado s.
"""
def valor_min(bot, s, alpha, beta, n):
  
  s.jogador = MIN # vez do gato

  if s.vitoria(MIN) or s.vitoria(MAX) or n > bot.max_profundidade:    
    return avaliacao(s)

  # ações disponíveis p/ o gato no estado s
  acoes = bot.acoes_gato(s)

  v = float('inf')

  for acao in acoes:
    s_suc = bot.resultado(s, acao)
    v = min(v, valor_max(bot, s_suc, alpha, beta, n+1))

    # Verifica a possibilidade da poda
    if v <= alpha:
      # Quando v <= alpha interrompe a expansão dos nós vizinhos restantes
      return v
    
    beta = min(beta,v)

  return v


"""
Implementa a função do jogador MAX do algoritmo minmax para determinar o valor de um estado s.

  :param <bot>: instância agente que controla os ratos.
  :param <s>: estado atual do jogo.
  :param <alpha>: o valor atual de alpha.
  :param <beta>: o valor atual de beta.
  :param <n>: a profundidade atual da busca.

  :returns: o valor da função de avaliação para o estado s.

"""
def valor_max(bot, s, alpha, beta, n):
  
  s.jogador = MAX # vez dos ratos
  s.rodada_inicial = False

  # obtém acções disponíveis p/ cada rato no estado "s"
  acoes = bot.acoes_rato(s)
  
  if s.vitoria(MIN) or s.vitoria(MAX) \
    or len(acoes) < 1 or n > bot.max_profundidade:      
      return avaliacao(s)
    

  # inicializa a lista que irá armazenar a avaliação do estado s
  # p/ cada ação disponível no turno dos ratos.
  melhor_a = [ float('-inf') for i in range(len(acoes))]    
  
  v = melhor_a[0]
  
  for i in range(len(acoes)):
    s_suc = bot.resultado(s, acoes[i])

    v = max(v, valor_min(bot, s_suc, alpha, beta, n+1))
    
    # Verifica a possibilidade de poda
    if v >= beta:
      # quando v >= beta interrompe a expansão dos nós vizinhos
      return v
    
    alpha = max(alpha,v)

    # melhor ação do rato i
    melhor_a[i] = v

  v = max(melhor_a)

  return v


#-----------------------------------------------------------------------------
# // fim MinMax
#-----------------------------------------------------------------------------
