# -*- coding: utf-8 -*-

# Instâncias
from src import Gato, Ratos, Tabuleiro, Ia_Ratos
# Métodos
from src import valida_movimento_gato, valida_movimento_ratos
from src import limpa_console, alerta_jogador
# constantes
from src import MAX, MIN
# algoritmo minmax
from minimax import minimax
# ferramentas auxiliares
from pprint import pprint
import time

"""-----------------------------------------------------------------------------
  Métodos para obter entradas na vez do humano
-----------------------------------------------------------------------------"""
def turno_humano():
  yx = None
  
  while(True):
  
    yx = input("  posicão: ")

    if len(yx) != 2:
      alerta_jogador("\t posicão inválida: a entrada deve conter 2 caracteres. ex: '4d'")
      
    else:
      break
  
  # essa validação ajusta a entrada para sempre ser (y,x)
  # Ex: mesmo o usuario entrando com "b4"
  # este condicional verifica e se necessário corrige para "4b"
  if yx[1].isnumeric():    
    y, x = yx[1].upper(), yx[0].upper()
  else:
    y, x = yx[0].upper(), yx[1].upper()
  
  # validação que garante um movimento válido para o gato
  valida_yx = valida_movimento_gato( gato, y, x, tabuleiro.celulas, True)
  if valida_yx:
    return valida_yx
  
  else:
   return turno_humano()


def turno_rato(bot, tabuleiro):  
  idx, y, x = minimax(bot)
  return idx, y, x


"""-----------------------------------------------------------------------------
 Executa o jogo
-----------------------------------------------------------------------------"""
if __name__ == "__main__":
  limpa_console()
  #----------------------------------------------
  # Inicializa instâncias
  #----------------------------------------------
  
  gato = Gato()
  gato.inicializar()
  
  ratos = Ratos()
  ratos.inicializar()
  
  tabuleiro = Tabuleiro()
  tabuleiro.inicializar( gato, ratos )
  
  bot = Ia_Ratos(ratos, gato, tabuleiro)

  #----------------------------------------------
  # Começa o jogo
  #----------------------------------------------
  
  # Jogo começa com ratos
  tabuleiro.jogador = MAX
  tabuleiro.rodada_inicial = True

  while(True):
    #limpa_console()
    #-----------------------------------------
    # VEZ do Rato
    #-----------------------------------------    
    if tabuleiro.jogador == MAX:
      
      print(" Vez do rato ... aguarde (10s)")
      idx, y, x = turno_rato(bot ,tabuleiro)
      
      # Caso em que n ratos == 1 e esta bloqueado
      if (idx, y, x) == ( -1, -1, -1):
        print("Ratos: Sem movimentos possíveis, passa vez...")
        tabuleiro.jogador = MIN        
        # considerar passar a vez para o gato. 
        continue
        
        # considera empate e finaliza o jogo:
        # break 

      tabuleiro.mover_rato(ratos, idx, y, x)
      tabuleiro.exibir()

      tabuleiro.rodada_inicial = False

      # Verifica condição de vitória após o último movimento do rato[idx]
      if tabuleiro.vitoria():          
        print(f"\n\t Você perdeu =\ \n")
        break

      tabuleiro.rodadas += 1      
      tabuleiro.jogador = MIN
      
      if tabuleiro.rodada_inicial == True:
        tabuleiro.rodada_inicial = False
      

    #-----------------------------------------
    # VEZ HUMANO
    #-----------------------------------------
    if tabuleiro.jogador == MIN:            
      print(" Sua vez:")
      y,x = turno_humano()            
      
      tabuleiro.mover_gato(gato, y, x)
            
      tabuleiro.exibir()

      if tabuleiro.vitoria():          
        print(f"\n\t Você venceu!\n")          
        break
      
      tabuleiro.rodadas += 1      
      tabuleiro.jogador = MAX

    

"""-----------------------------------------------------------------------------
# // fim.
-----------------------------------------------------------------------------"""
