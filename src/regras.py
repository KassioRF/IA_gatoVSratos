
"""-----------------------------------------------------------------------------
 Módulo que implementa os métodos para a validação dos movimentos
 dos jogadores de acordo com as regras.
-----------------------------------------------------------------------------"""

from .util import *
from .constants import COLUNAS, GATOICON

"""-----------------------------------------------------------------------------
 Valida o formato das coordenadas de entrada (y,x)

  :param <y>: uma string que representa uma linha válida no 
              intervalo [1, 8].
  
  :param <x>: uma string que representa uma coluna válida no conjunto 
              ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'].

  :return: retorna True se as coordenadas são válidas ou False caso contrário.

-----------------------------------------------------------------------------"""
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

"""-----------------------------------------------------------------------------
 Função que valida o movimento do gato no tabuleiro de acordo com as regras 
 de movimento do jogo.

  :param <gato>: class <src.jogadores.gato> instância do objeto que mantém as 
                informações do gato no jogo.

  :param <y>: inteiro que faz referência a uma linha p/ nova posição ([1,...8]).
  
  :param <x>: string que faz referência a uma coluna p/ nova posição ([A,..,H]).

  :param <celulas>: dicionário que armazena a estrutura das células do tabuleiro.

  :param <feedback>: quando True ativa as mensagens de feedback para o jogador
                    ( caso as coordenadas inseridas forem inválidas ).
  
  :return: um par de valores (y, x) se o movimento é válido, ou 'False' 
            caso contrário.
  
  :example: 
    se a posição atual do gato é (1, 'D') e o jogador deseja mover o rato para 
    a posição (7, 'D'), a função retorna um par de valores (7, 'D') se o 
    movimento é válido, ou 'False' caso contrário.
-----------------------------------------------------------------------------"""
def valida_movimento_gato(gato, y, x, celulas, feedback=False):

  # primeiro verifica se os valores y e x estão no formato de entrada correto.
  valida_yx = valida_coordenadas(y,x)
  if not valida_yx:
    return False

  y,x = valida_yx

  # Exige um movimento diferente da pos atual.
  if gato.pos == (y,x):
    if feedback:
      alerta_jogador("O movimento deve ser diferente da posição atual")
    
    return False

  # Proíbe movimentos diagonais
  elif gato.pos[0] != y and gato.pos[1] != x:
    if feedback:
      alerta_jogador("Movimento diagonal nao permitido")
    
    return False
  

  # Proibe o movimento onde exista um rato no trajeto.
  
  # Caso 1: É um movimento horizontal (x)
  elif gato.pos[0] == y:    
    
    origem, destino = (gato.pos[1], x) if gato.pos[1] < x else (x, gato.pos[1])

    ''' As coordenadas x sao letras contidas no conjunto COLUNAS
    acessamos a coordenada no tabuleiro com a letra COLUNAS[indice]
    mas caminhamos pelas céluas (x+n, x-n) com os indices de COLUNAS. '''
    origem, destino = COLUNAS.index(origem), COLUNAS.index(destino),
    
    # Verifica obstáculo no intervalo [ origem + 1, destino - 1 ]
    for xx in range(origem + 1, destino):
      
      if celulas[y, COLUNAS[xx]] != None:
        if feedback:
          alerta_jogador("Obstáculo no caminho ")
        
        return False

  # Caso 2: É um movimento vertical (y)
  elif gato.pos[1] == x:
  
    # Verifica obstáculo no intervalo [origem+1, destino+1]
    origem, destino = (gato.pos[0], y) if gato.pos[0] < y else (y, gato.pos[0])

    for yy in range(origem + 1, destino):
      
      if celulas[yy, x] != None:
        if feedback:
          alerta_jogador("Obstáculo no caminho ")
        
        return False
  
  # Movimento válido
  return y,x


"""-----------------------------------------------------------------------------
 Função que valida o movimento de um rato no tabuleiro de acordo com as regras 
 de movimento do jogo.

  :param <ratos_pos> : tupla (y,x) posição atual do rato.
  
  :param <y>: inteiro que faz referência a uma linha p/ nova posição ([1,...8]).
  
  :param <x>: string que faz referência a uma coluna p/ nova posição ([A,..,H]).
  
  :param <celulas>: dicionário que armazena a estrutura das células do tabuleiro.
  
  :param <rodada_inicial>: informa se é um movimento realizado na primeira 
                           rodada do jogo (mantém o valor padrão como False).

  :return: um par de valores (y, x) se o movimento é válido, ou 'False' 
            caso contrário.

  :example: 
    se a posição atual do rato é (2, 'B') e o jogador deseja mover o rato para 
    a posição (1, 'B'), a função retorna um par de valores (1, 'B') se o 
    movimento é válido, ou 'False' caso contrário.
-----------------------------------------------------------------------------"""
def valida_movimento_ratos(rato_pos, y, x, celulas, rodada_inicial=False):

  # primeiro verifica se os valores y e x estão no formato de entrada correto.
  if not valida_coordenadas(y,x):
    return False

  # Exige um movimento diferente da pos atual.
  if rato_pos[0] == y and rato_pos[1] == x :
    return False

  # Permite o movimento na diagonal se e somente se existir um gato em:
  # (y - 1, x - 1) ou (y - 1, x + 1).
  if rato_pos[0] != y and rato_pos[1] != x:

    if celulas[ y, x] != GATOICON:
      return False

  # Garante o movimento tamanho |1| :: ( y - 1) e
  # permite movimento tamanho 2 para a primeira rodada  
  if rato_pos[0] - 1 > y:
  
    if rodada_inicial and rato_pos[0] - 2 == y:
      pass
  
    else:
      return False

  # Garante que a celula da frente esteja livre
  if celulas[ y, x ] != None and rato_pos[1] == x:
    return False
  
  
  return y, x

