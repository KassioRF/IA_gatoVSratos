
from src import LINHAS, COLUNAS, RATOICON, MIN, MAX
from src import valida_movimento_gato, verifica_capturaR
from src import print_celulas


"""============================================================================= 
 HEURISTICA:

  Availa a quantidade de rodadas necessárias para o gato ganhar.



============================================================================="""
def heuristica(s):

  dist_g = [ 0 for i in range(s.ratos.n)]
  
  # Quantas rodadsa pro gato ganhar?
  for i in range(s.ratos.n):    
    y, x = s.ratos.pos[i]

    g_captura = valida_movimento_gato(s.gato, y, x, s.celulas)
    
    if g_captura:

      xx = COLUNAS.index(x)

      # se se rato protegido: vantagem pro rato
      if xx - 1 > 0 and xx + 1 < LINHAS:
        if s.celulas[ y + 1 , COLUNAS[xx-1] ] == RATOICON \
          or s.celulas[ y + 1 , COLUNAS[xx+1] ] == RATOICON:

            dist_g[i] += 2.5

      else:
        # pelo menos 1 jogada p/ capturar o rato i
        dist_g[i] += 1

    else:
      # pelo menos 2 jogadas p/ capturar rato i
      dist_g[i] += 2


  vG = sum(dist_g) / s.ratos.n

  # vR -= 1 if s.jogador == MAX else 0
  # vG -= 1 if s.jogador == MIN else 0

  return vG

#=============================================================================
#=============================================================================


