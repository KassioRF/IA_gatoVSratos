
# Instâncias
from src import gato, ratos, bot, tabuleiro
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
  
    yx = input("\t posicao: ")

    if len(yx) != 2:
      alerta_jogador("\t posicao inválida: o formato deve ser '4d' ")
      
    else:
      break

  return yx[0].upper(), yx[1].upper()



def turno_rato():
  pass

"""-----------------------------------------------------------------------------
  Executa o jogo
-----------------------------------------------------------------------------"""
from pprint import pprint
if __name__ == "__main__":  
  print("refatorando")
  #----------------------------------------------
  # Inicializa instâncias
  #----------------------------------------------
  gato.inicializar()
  ratos.inicializar()

  tabuleiro.inicializar( gato, ratos )

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
      print(f"\n ====== RODADA: {rodada} ========")
      rodada += 1

      #-----------------------------------------
      # Escolhe um rato idx e coordenadas (y,x) 
      #-----------------------------------------
      while(True):
        idx, y, x = bot.escolhe_rato()
        # Quando nao ha movimentos disponiveis
        if (idx, y, x) == ( -1, -1, -1):
          break

        # Se a coordenada do laço é valida prossegue para a etapa de movimento
        if valida_movimento_ratos(ratos.pos[idx], y, x):
          break

      
      # Caso em que n ratos == 1 e esta bloqueado
      if (idx, y, x) == ( -1, -1, -1):
        print("Ratos: Sem movimentos possíveis, passa a vez...")
        tabuleiro.jogador = MIN
        continue

      #-----------------------------------------
      # Executa o movimento com y,x válidos 
      #-----------------------------------------
      if tabuleiro.mover_rato(ratos, idx, y, x):
        # limpa_console()
        tabuleiro.exibir()

        # Verifica condicao de vitoria após o último movimento do rato[idx]
        if tabuleiro.vitoria(idx):          
          print(f"\n\t Você perdeu =\ \n")
          break

      tabuleiro.jogador = MIN

    #-----------------------------------------
    # VEZ HUMANO
    #-----------------------------------------
    if tabuleiro.jogador == MIN:            
      print(f"\n ====== RODADA: {rodada} ========")
      rodada += 1

      # obtém coordenadas
      y,x = turno_humano()
      
      valida_yx = valida_movimento_gato( gato, y, x)
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

        tabuleiro.jogador = MAX


  #----------------------------------------------
  # testar movimento ratos e gatos
  #----------------------------------------------
