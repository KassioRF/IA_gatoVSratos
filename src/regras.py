"""
  Neste Modulo são aplicadas as regras de movimento, captura e 
  condições de vitória do jogo.
"""
#------------------------------------------------------------------------------
# Valida coordenadas o formato das coordenadas
#------------------------------------------------------------------------------
from src.constants import *
from src.util import *

def valida_coordenadas(y,x):
  
  x = x.upper()  
  # Garante que y é inteiro
  if type(y) != int:
    return False  
  
  # Garante que y está no intervalo [1,8]
  elif y < 1  or y > 8:
    return False
  
  # Garante que x é não vazio
  elif not x or x == "":
    return False

  # Garante que x é string
  elif type(x) != str:
    return False

  # Garante que x está no intervalo [A,..,H]
  elif x not in REFCOL:
    return False

  
  return True


#------------------------------------------------------------------------------
# Verifica as regras antes de realizar o movimento do gato
#------------------------------------------------------------------------------
def valida_movimento_gato(tabuleiro, gato, y, x):
  
  if not valida_coordenadas(y,x):
    return False

  # @ DUVIDA: O jogador pode passar a vez ?
  # Assumindo que cada rodada deve haver um movimento
  if gato.pos == (y,x):
    alerta_jogador("O movimento deve ser diferente da posição atual")
    return False

  # Proíbe movimentos diagonais
  elif gato.pos[0] != y and gato.pos[1] != x:
    alerta_jogador("Movimento diagonal nao permitido")
    return False
  
  # Proibe caminho com um rato no trajeto

  # Caso 1: É um movimento horizontal (x)
  elif gato.pos[0] == y:    
    # Verifica obstáculo no intervalo origem+1 destino-1
    origem, destino = (gato.pos[1], x) if gato.pos[1] < x else (x, gato.pos[1])
    
    # As coordenadas x sao letras contidas no conjunto REFCOL
    # Por isso caminhamos pelas céluas com os indices de REFCOL
    # E acessamos a coordenada no tabuleiro com a letra REFCOL[indice]

    origem, destino = REFCOL.index(origem), REFCOL.index(destino),
    
    for xx in range(origem + 1, destino):
      if tabuleiro[y, REFCOL[xx]] != None:
        alerta_jogador("Obstáculo no caminho ")
        return False

  # Caso 2: É um movimento vertical (y)
  elif gato.pos[1] == x:
    # Verifica obstáculo no intervalo origem+1 destino+1
    origem, destino = (gato.pos[0], y) if gato.pos[0] < y else (y, gato.pos[0])

    for yy in range(origem + 1, destino):
      if tabuleiro[yy, x] != None:
        alerta_jogador("Obstáculo no caminho ")
        return False
  

  return True


#------------------------------------------------------------------------------
# Verifica as regras antes de realizar o movimento de um rato
#------------------------------------------------------------------------------
def valida_movimento_ratos(tabuleiro, rato_pos, y, x):

  if not valida_coordenadas(y,x):
    return False


  # Exije um movimento
  if rato_pos[0] == y and rato_pos[1] == x :
    alerta_jogador("O movimento deve ser diferente da posição atual")
    return False

  # Garante o movimento na diagonal se e somente se existir um gato em:
  # (y, x - 1) ou (y, x + 1) 
  if rato_pos[0] != y and rato_pos[1] != x:
    if tabuleiro[ y, x] != "&":
      alerta_jogador("Movimento inválido")
      return False

 
  # Garante movimento para frente
  if rato_pos[0] == y and rato_pos[1] != x :
    alerta_jogador("Movimento lateral não é permitido para ratos")
    return False
  
  #  invalida movimentos para tras
  if rato_pos[0] < y:
    alerta_jogador("Movimento inválido")
    return False

  # Garante o movimento tamanho 1 : y == y - 1 e
  # permite movimento tamanho 2 para a primeira rodada
  if rato_pos[0] - 1 > y:
    if RODADAINICIAL and rato_pos[0] - 2 == y:
      pass
    else:
      alerta_jogador("Movimento inválido")
      return False

  # Garante que a celula da frente esteja livre
  if rato_pos[0] == y and tabuleiro[ y, x ] != None :
      alerta_jogador("Movimento inválido: Obstáculo")
      return False


  return True
