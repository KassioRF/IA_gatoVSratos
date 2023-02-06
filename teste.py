
# Instâncias
# from src import gato, ratos, bot, tabuleiro
from src import Gato, Ratos, Tabuleiro, Ia_Ratos
# Métodos
from src import valida_movimento_gato, valida_movimento_ratos
from src import limpa_console, alerta_jogador
# constantes
from src import MAX, MIN


"""-----------------------------------------------------------------------------
  Métodos para obter coordenadas
-----------------------------------------------------------------------------"""
def turno_humano():
  yx = None
  
  while(True):
  
    yx = input("  posicão: ")

    if len(yx) != 2:
      alerta_jogador("\t posicão inválida: a entrada deve conter 2 caracteres. ex: '4d' ")
      
    else:
      break
  
  if yx[1].isnumeric():    
    return yx[1].upper(), yx[0].upper()
  else:
    return yx[0].upper(), yx[1].upper()



#@TODO a construção desse metodo poder mudar com o uso de MIN MAX
def turno_rato(tabuleiro):
  
  idx, y, x = bot.minimax()
  # idx, y, x = bot.escolhe_rato()

  return idx, y, x


"""-----------------------------------------------------------------------------
  Executa o jogo
-----------------------------------------------------------------------------"""
from pprint import pprint
import time



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
  rodada = 0
  capturados = 0
  
  # Jogo começa com ratos
  tabuleiro.jogador = MAX
  while(True):
    #-----------------------------------------
    # VEZ do Rato
    #-----------------------------------------
    if tabuleiro.jogador == MAX:
      print(f"\t ====== RODADA: {rodada} ========")

      #-----------------------------------------
      # Escolhe um rato idx e coordenadas (y,x) 
      #-----------------------------------------
      idx, y, x = turno_rato(tabuleiro)
      
      # Caso em que n ratos == 1 e esta bloqueado
      if (idx, y, x) == ( -1, -1, -1):
        print("Ratos: Sem movimentos possíveis, Empate...")
        tabuleiro.jogador = MIN
        break

      #-----------------------------------------
      # Executa o movimento com y,x válidos 
      #-----------------------------------------
      if tabuleiro.mover_rato(ratos, idx, y, x):
        # limpa_console()
        tabuleiro.exibir()

        # Verifica condicao de vitoria após o último movimento do rato[idx]
        if tabuleiro.vitoria():          
          print(f"\n\t Você perdeu =\ \n")
          break

      rodada += 1
      
      tabuleiro.jogador = MIN
      
      if tabuleiro.rodada_inicial == True:
        tabuleiro.rodada_inicial = False
      
      # break

    #-----------------------------------------
    # VEZ HUMANO
    #-----------------------------------------
    if tabuleiro.jogador == MIN:            
      print(f"\t ====== RODADA: {rodada} ========")

      # obtém coordenadas
      y,x = turno_humano()
      
      valida_yx = valida_movimento_gato( gato, y, x, tabuleiro.celulas)
      # validação formata os valoes, como parse int para y etc..
      if valida_yx:

        y, x = valida_yx
        
        # Executa o movimento no tabuleiro
        tabuleiro.mover_gato(gato, y, x)

        # limpa_console()
        tabuleiro.exibir()

        if tabuleiro.vitoria():          
          print(f"\n\t Você venceu!\n")          
          break
        
        rodada += 1
        
        tabuleiro.jogador = MAX
      else:
        continue


      # limpa_console()

  #----------------------------------------------
  # testar movimento ratos e gatos
  #----------------------------------------------
