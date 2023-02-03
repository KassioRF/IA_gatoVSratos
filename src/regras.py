"""
  Neste Modulo são aplicadas as regras de movimento, captura e 
  condições de vitória do jogo.
"""


from src.jogadores import *
from src.constants import *
from src.util import *
from main import Tabuleiro

#------------------------------------------------------------------------------
# Valida o formato das coordenadas (int, str) ::: ([1,...8], [A,...H])
#------------------------------------------------------------------------------
def valida_coordenadas(y,x):
  

  x = x.upper()  
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
  if x not in Tabuleiro.Cols:
    alerta_jogador("A Coluna deve ser uma letra entre [A,..,H]")
    return False

  return y,x


#------------------------------------------------------------------------------
# Verifica as regras antes de realizar o movimento do gato
#------------------------------------------------------------------------------
def valida_movimento_gato(tabuleiro, gato, y, x):
  valida_yx = valida_coordenadas(y,x)
  if not valida_yx:
    return False

  y,x = valida_yx

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
    
    # As coordenadas x sao letras contidas no conjunto Tabuleiro.Cols
    # Por isso caminhamos pelas céluas com os indices de Tabuleiro.Cols
    # E acessamos a coordenada no tabuleiro com a letra Tabuleiro.Cols[indice]

    origem, destino = Tabuleiro.Cols.index(origem), Tabuleiro.Cols.index(destino),
    
    for xx in range(origem + 1, destino):
      if tabuleiro[y, Tabuleiro.Cols[xx]] != None:
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
  

  return y,x


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
    # if tabuleiro[ y, x] != "&":
    if tabuleiro[ y, x] != Gato.icon:
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
    if Tabuleiro.rodada_inicial and rato_pos[0] - 2 == y:
      pass
    else:
      alerta_jogador("Movimento inválido")
      return False

  # Garante que a celula da frente esteja livre
  if tabuleiro[ y, x ] != None and rato_pos[0] == x  :
      alerta_jogador("Movimento inválido: Obstáculo")
      return False


  return y, x
