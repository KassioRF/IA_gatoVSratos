from src import LINHAS, COLUNAS, RATOICON, MIN, MAX
from src import valida_movimento_gato
from src import print_celulas


"""-----------------------------------------------------------------------------
 HEURÍSTICA Para a busca imperfeita em tempo real do algorítimo MinMax
  
  Esta função avalia a probabilidade de vitória para os jogadores a partir de um
  estado s qualquer.

  A abordagem utilizada considera a diferença entre a quantidade de rodadas
  ( distância ) necessárias para o jogador MAX ou MIN vencer o jogo.

-----------------------------------------------------------------------------"""

def heuristica(s):

  """--------------------------------------------------------------------------------------
  Lista que irá armazenar a quantidade de rodadas necessárias para o gato capturar cada rato.
  -----------------------------------------------------------------------------------------"""
  dist_g = [ 0 for i in range(s.ratos.n)]

  """--------------------------------------------------------------------------------------
  Lista que armazenará a quantidade de rodadas necessárias para cada rato chegar 
  à linha 1 do tabuleiro.

  -----------------------------------------------------------------------------------------"""
  dist_r = [ 0 for i in range(s.ratos.n)]

  for i in range(s.ratos.n):    
    y, x = s.ratos.pos[i]

    # se o rato i está na mesma linha ou coluna do gato (sem obstáculos)
    # a distância para a captura é de apenas 1 movimento
    g_captura = valida_movimento_gato(s.gato, y, x, s.celulas)
    
    if g_captura:
      dist_g[i] = 1
    # caso contrário a distância para a captura é de 2 movimentos
    else:
      dist_g[i] = 2

    # obtém a distância do rato i até o a linha 1 do tabuleiro
    # considera a distância do gato até o rato i como um peso adicional
    dist_r[i] = abs(y-7)/7 + dist_g[i]
   
  """--------------------------------------------------------------------------------------
  Calcula a diferença entre a soma das distâncias dos ratos até a linha 1 do tabuleiro e 
  a soma das distâncias entre o gato e cada rato, representando 
  assim a probabilidade de vitória do jogador MAX.
  -----------------------------------------------------------------------------------------"""
  vG = sum(dist_r) - sum(dist_g)


  return vG

#=============================================================================
#=============================================================================
