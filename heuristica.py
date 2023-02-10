
from src import LINHAS, COLUNAS, RATOICON, MIN, MAX
from src import valida_movimento_gato, verifica_capturaR
from src import print_celulas


"""-----------------------------------------------------------------------------
 HEURÍSTICA Para a busca imperfeita em tempo real do algorítimo MinMax

  Availa a quantidade de rodadas necessárias para o gato ganhar.

  Quanto maior a média de rodadas necessárias para o gato ganhar
  mais chances algum rato terá de chegar no final.

  É importante levar em consideração estados do tabuleiro onde 
  existem ratos protegidos de captura, ou seja com outro rato 
  em [ (y + 1), ( x - 1 ou x + 1) ]

  Nestes casos a distância de captura aumenta, mesmo o gato estando
  na mesma linha ou coluna do rato.

-----------------------------------------------------------------------------"""
def heuristica(s):

  dist_g = [ 0 for i in range(s.ratos.n)]
  
  # Quantas rodadas pro gato ganhar?

  # Para cada rato no tabuleiro verifica a distância necessária 
  # para capturá-lo
  for i in range(s.ratos.n):    
    y, x = s.ratos.pos[i]

    # se o movimento do gato para a coordenada do rato i for válido,
    # então existe um movimento de captura contra este rato.
    g_captura = valida_movimento_gato(s.gato, y, x, s.celulas)
    
    if g_captura:

      xx = COLUNAS.index(x)

      if xx - 1 > 0 and xx + 1 < LINHAS:
        if s.celulas[ y + 1 , COLUNAS[xx-1] ] == RATOICON \
          or s.celulas[ y + 1 , COLUNAS[xx+1] ] == RATOICON:

            # se rato protegido: vantagem p/ o rato
            dist_g[i] += 2 + abs(y-7)/7
            # dist_g[i] += 2 - abs(y-1)/10

      else:
        # se rato desprotegido: vantagem p/ o gato
        dist_g[i] += 1

    else:
      # pelo menos 2 jogadas p/ capturar o rato i
      # ratos com y mais proximos de 1 tem prioridade
      dist_g[i] += 2 + abs(y-7)/7


  # quantidade média de rodadas p/ o gato varrer os ratos do mapa.
  vG = sum(dist_g) 


  return vG

#=============================================================================
#=============================================================================


