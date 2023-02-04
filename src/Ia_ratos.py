

"""-----------------------------------------------------------------------------
 Classe IA_Ratos
 Controla os ratos no tabuleiro
-----------------------------------------------------------------------------"""
class Ia_Ratos():
  
  # rato escolhido para o movimento
  escolhido = 0

  def __init__(self, ratos, gato, tabuleiro):
    self.ratos = ratos
    self.gato = gato
    self.tabuleiro = tabuleiro

  # ------------------------------------------------------------------
  # Verifica se o gato está na diagonal inferior esquerda ou direita
  # em relação a posicão atual do rato idx.
  #
  # a captura é valida se:
  # gato está em:
  # Caso 1: [y-1, x-1]; Caso 2: [ y-1, x+1 ]; para x,y :: [1,...,8]
  #
  # idx: índice do rato contido na lista de posicoes para os ratos
  # ------------------------------------------------------------------
  def movimento_captura(self, idx):
  
    ratoy = self.ratos.pos[idx][0]
    gatoy = self.gato.pos[0]

    # conversão da letra da coluna para o índice respectivo da letra
    gatox = self.tabuleiro.Cols.index(self.gato.pos[1])
    ratox = self.tabuleiro.Cols.index(self.ratos.pos[idx][1])

    # se gato nao está 1 linha abaixo a captura já é invalida
    if gatoy == ratoy  - 1:
      # Caso 1:
      if gatox  == ratox - 1:
        print("caso1")

        y, x = self.ratos.pos[idx]
        y = y - 1      
        x = self.tabuleiro.Cols[ratox - 1] 
        return y, x
    
      # Caso 2:
      elif gatox == ratox + 1 :
        print("caso2")
        
        y, x = self.ratos.pos[idx]
        y = y - 1
        x = self.tabuleiro.Cols[ratox + 1]
        return y, x

    return [ -1, -1 ]

  # ------------------------------------
  # Escolhe o rato e o movimento a ser realizado
  # Caso 1: Existe movimento de captura ( MAIOR PRIORIDADE )
  # Caso 2: Primeiro movimento do jogo, entao permite mover ate 2 casas
  # Caso 3: movimenta 1 casa para frente
  #
  # @TODO separar o caso 2 em outro metodo ? reduziria o numero de verificaoes?
  #
  # Retorna: (idx do rato, linha, coluna)
  # ------------------------------------
  
  def escolhe_rato(self):
    
    # teste captura (Caso 1)
    for idx in range(self.ratos.n):
      y, x =  self.movimento_captura(idx)
      # encontrou uma captura!
      # print(y,x)
      if (y,x) != (-1,-1):
        return idx, y, x

        
    # o id do escolhido
    idx = self.escolhido % self.ratos.n    
    # atualiza a próxima escolha
    self.escolhido += 1

    # atribui o movimento
    y, x = self.ratos.pos[idx]

    # Caso 2:
    if self.tabuleiro.rodada_inicial:
      y = y - 2
      
      return idx, y, x
    
    # Caso 3:
    # Obs: Se houver somente 1 rato no tabuleiro e, 
    # um gato estiver em (y - 1, x), o rato passa a vez
    y = y - 1
    if self.ratos.n == 1 and self.gato.pos == (y,x):      
      return -1, -1, -1
    
    elif self.gato.pos == (y,x):
      return self.escolhe_rato()

    return idx, y, x
      
  

