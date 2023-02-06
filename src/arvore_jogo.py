
"""
Arvore de jogo
Cada nó é um tabuleiro
"""
class No:
    
  def __init__(self, pai, estado, jogador, utilidade, nivel ):
    self.jogador = jogador
    self.pai = pai
    self.estado = estado
    self.utilidade = utilidade
   
    

"""
Exploração em profundidade da arvore do jogo
"""
class PilhaFronteira:
  def __init__(self):
    self.fronteira = []

  # inserir na pilha
  def add(self, no):
    self.fronteira.append(no)

  def contem_estado(self, estado):
    return any(no.estado == estado for no in self.fronteira)
  
  # Verifica se a Fronteira esta vazia
  def isEmpty(self):
    return len(self.fronteira) == 0

  # Remove estado da Fronteira do tipo Pilha
  def remove(self):
    if self.isEmpty():
      raise Exception("Fronteira vazia")
    else:
      no = self.fronteira[-1]
      self.fronteira = self.fronteira[:-1]
      return no
