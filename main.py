# -*- coding: utf-8 -*-

# Instâncias
# from src import gato, ratos, bot, tabuleiro
from src import Gato, Ratos, Tabuleiro, Ia_Ratos
# Métodos
from src import valida_movimento_gato, valida_movimento_ratos
from src import limpa_console, alerta_jogador
# constantes
from src import MAX, MIN
# ferramentas
from pprint import pprint
import time

"""-----------------------------------------------------------------------------
  Métodos para obter coordenadas
-----------------------------------------------------------------------------"""
def turno_humano():
  yx = None
  
  while(True):
  
    yx = input("  posicão: ")

    if len(yx) != 2:
      alerta_jogador("\t posicão inválida: a entrada deve conter 2 caracteres. ex: '4d' ", True)
      
    else:
      break
  
  if yx[1].isnumeric():    
    # return yx[1].upper(), yx[0].upper()
    y, x = yx[1].upper(), yx[0].upper()
  else:
    # return yx[0].upper(), yx[1].upper()
    y, x = yx[0].upper(), yx[1].upper()
  
  # validação formata os valoes, como parse int para y etc..
  valida_yx = valida_movimento_gato( gato, y, x, tabuleiro.celulas, True)
  if valida_yx:
    return valida_yx
  
  else:
   return turno_humano()


#@TODO a construção desse metodo poder mudar com o uso de MIN MAX
def turno_rato(tabuleiro):  
  # idx, y, x = bot.escolhe_rato()
  idx, y, x = bot.minimax()
  
  return idx, y, x


"""-----------------------------------------------------------------------------
 # Executa o jogo
-----------------------------------------------------------------------------"""
#@TODO Ajustar limpa console para 2 turnos ( 1 rodada )
if __name__ == "__main__":
  print("refatorando")
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
  
  while(True):
    #-----------------------------------------
    # VEZ do Rato
    #-----------------------------------------
    if tabuleiro.jogador == MAX:

      idx, y, x = turno_rato(tabuleiro)
      
      # Caso em que n ratos == 1 e esta bloqueado
      if (idx, y, x) == ( -1, -1, -1):
        print("Ratos: Sem movimentos possíveis, Empate...")
        tabuleiro.jogador = MIN        
        # considera empate
        break 
        # considerar passar a vez para o gato. Consequentemente é vitória do gato
        # no proximo.
        # continue

      tabuleiro.mover_rato(ratos, idx, y, x)
      tabuleiro.exibir()

      # Verifica condicao de vitoria após o último movimento do rato[idx]
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
