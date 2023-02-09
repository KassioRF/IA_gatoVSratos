from src.util import limpa_console, print_celulas
from src import RATOICON, GATOICON, LINHAS, COLUNAS

def exibir(celulas):
  # padrao celula vazia
  celula_vazia = "___|"
  
  # borda superior    
  print("\n")
  line = "  " + "_"*32
  print(line)
    
  # células
  for y in reversed(range(LINHAS+1)):
    line = ""
    for x in range(LINHAS+1):
      # deixa em branco (0,0)                
      if y == 0 and x == 0:
        line += "  "
        continue
      
      # referência visual para as colunas [A,H] 
      elif y == 0 and x > 0:
        line += f" {COLUNAS[x - 1]}  "
      
      # referência visual para as linhas: [8,1]
      elif x == 0:
        line += f"{y}|"

      # pos do gato
      elif celulas[ y, COLUNAS[x - 1] ] != None:
        line += f"_{celulas[y, COLUNAS[x - 1]]}_|"

      else:
        line += celula_vazia

    print(line)
  
  print("\n")


if __name__ == "__main__":
  limpa_console()

  print(':::: Testes :::: ')
  def cel():
    celulas = { (y,x) : '_'
      for x in COLUNAS
      for y in range(1, LINHAS + 1) }
    return celulas

  
  ry, rx = 5, 0

  gy, gx = 7, 4
  
  # #ratos
  celulas = cel()

  # # ratos
  # celulas[ 7, "A" ] = RATOICON
  # celulas[ 6, "B" ] = RATOICON
  # celulas[ 5, "C" ] = RATOICON
  # celulas[ 5, "F" ] = RATOICON
  # celulas[ 6, "G" ] = RATOICON
  # celulas[ 7, "H" ] = RATOICON
  
  # # gato
  # celulas[ 7, "D" ] = GATOICON
  
  # ratos
  # celulas[ 2, "F" ] = RATOICON
    # ratos
  celulas[ 4, "A" ] = RATOICON
  celulas[ 4, "B" ] = RATOICON
  celulas[ 4, "G" ] = RATOICON

  # gato
  celulas[ 3, "E" ] = GATOICON


  exibir(celulas)

# ( Li >  r i-1 )