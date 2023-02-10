"""-----------------------------------------------------------------------------
 Neste Módulo são aplicadas a validação dos movimentos
 dos jogadores de acordo com as regras.
-----------------------------------------------------------------------------"""

from .util import *
from .constants import COLUNAS, GATOICON

#------------------------------------------------------------------------------
# Valida o formato das coordenadas (int, str) ::: ([1,...8], [A,...H])
#------------------------------------------------------------------------------
def valida_coordenadas(y,x):
  
  # Garante que y é inteiro
  if type(y) != int:
    try:
      y = int(y)
    except:
      alerta_jogador("A linha deve ser um inteiro entre [1,..,8]")
      return False  
  
  # Garante que y está no intervalo [1,8]
  if y not in range(1, 9):
    alerta_jogador("A linha deve ser um inteiro entre [1,..,8]")
    return False
  
  # Garante que x é não vazio
  if not x or x == "":
    return False

  # Garante que x é string
  if type(x) != str:
    alerta_jogador("A Coluna deve ser uma letra entre [A,..,H]")
    return False

  # Garante que x está no intervalo [A,..,H]
  if x not in COLUNAS:
    alerta_jogador("A Coluna deve ser uma letra entre [A,..,H]")
    return False

  return y,x

#------------------------------------------------------------------------------
# Verifica as regras antes de realizar o movimento do gato
# feedback exibido apenas no jogo humano
#------------------------------------------------------------------------------
def valida_movimento_gato(gato, y, x, celulas, feedback=False):

  valida_yx = valida_coordenadas(y,x)

  if not valida_yx:
    return False

  y,x = valida_yx

  # Assumindo que cada rodada deve haver um movimento
  if gato.pos == (y,x):
    alerta_jogador("O movimento deve ser diferente da posição atual", feedback)
    return False

  # Proíbe movimentos diagonais
  elif gato.pos[0] != y and gato.pos[1] != x:
    alerta_jogador("Movimento diagonal nao permitido", feedback)
    return False
  

  # Proibe caminho com um rato no trajeto
  # Caso 1: É um movimento horizontal (y)
  elif gato.pos[0] == y:    
    # Verifica obstáculo no intervalo origem+1 destino-1
    origem, destino = (gato.pos[1], x) if gato.pos[1] < x else (x, gato.pos[1])
    
    # As coordenadas x sao letras contidas no conjunto COLUNAS
    # acessamos a coordenada no tabuleiro com a letra COLUNAS[indice]
    # mas caminhamos pelas céluas (x+n, x-n) com os indices de COLUNAS
    origem, destino = COLUNAS.index(origem), COLUNAS.index(destino),
    
    for xx in range(origem + 1, destino):
      
      if celulas[y, COLUNAS[xx]] != None:
        alerta_jogador("Obstáculo no caminho ", feedback)
        return False

  # Caso 2: É um movimento vertical (x)
  elif gato.pos[1] == x:
  
    # Verifica obstáculo no intervalo [origem+1, destino+1]
    origem, destino = (gato.pos[0], y) if gato.pos[0] < y else (y, gato.pos[0])

    for yy in range(origem + 1, destino):
      
      if celulas[yy, x] != None:
        alerta_jogador("Obstáculo no caminho ", feedback)
        return False
  
  # Movimento válido
  return y,x

#------------------------------------------------------------------------------
# Verifica as regras antes de realizar o movimento de um rato
#------------------------------------------------------------------------------
def valida_movimento_ratos(rato_pos, y, x, celulas, rodada_inicial=False):

  if not valida_coordenadas(y,x):
    return False

  # Exije um movimento diferente da pos atual
  if rato_pos[0] == y and rato_pos[1] == x :
    alerta_jogador("O movimento deve ser diferente da posição atual")
    return False

  # Permite o movimento na diagonal se e somente se existir um gato em:
  # (y, x - 1) ou (y, x + 1) 
  if rato_pos[0] != y and rato_pos[1] != x:

    if celulas[ y, x] != GATOICON:
      alerta_jogador("Movimento inválido 1")
      return False

  # Garante movimento para frente
  if rato_pos[0] == y and rato_pos[1] != x :
    alerta_jogador("Movimento lateral não é permitido para ratos")
    return False
  
  #  invalida movimentos para trás
  if rato_pos[0] < y:
    alerta_jogador("Movimento inválido 2")
    return False

  # Garante o movimento tamanho |1| :: ( y - 1) e
  # permite movimento tamanho 2 para a primeira rodada  
  if rato_pos[0] - 1 > y:
  
    if rodada_inicial and rato_pos[0] - 2 == y:
      pass
  
    else:
      alerta_jogador("Movimento inválido 3")
      return False

  # Garante que a celula da frente esteja livre
  if celulas[ y, x ] != None and rato_pos[1] == x:
    alerta_jogador("Movimento inválido: Obstáculo")
    return False
  
  # Movimento válido!
  return y, x

#------------------------------------------------------------------------------
# verifica se existe um gato passível de captura para uma acao "a" do rato
# :param: <acao> = (idx, y, x), idx é o indice do rato
#------------------------------------------------------------------------------
def verifica_capturaR(acao, estado):
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