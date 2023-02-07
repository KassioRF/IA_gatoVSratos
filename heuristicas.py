#===============================================================================
# Não captura e não matém postura defensiva
def heuristica(self, s):
  vantagem = 0
  desvantagem = 0

  gy, _gx = s.gato.pos
  gx = s.Cols.index(_gx)

  # ry, _rx = s.ratos.pos[idx]
  # rx = s.Cols.index(_rx)
  # yy, _xx = s.ratos.pos[ii]
  # xx = s.Cols.index(_xx)

  # n Turnos p/ rato ganhar
  ratos_restantes = s.ratos.n
  v_gatos = 0
  v_ratos = 0


  for idx in range(s.ratos.n):
    ry, _rx = s.ratos.pos[idx]
    rx = s.Cols.index(_rx)
    
    # ---------- GATO ----------------- #
    # Categoria do estado: em quantas rodadas gato ganha ?
    # Caso 1: movimento horizontal (y)
    if gy == ry:
      # se tem um rato (y + 1) ( x - 1) ou ( x + 2)
      if rx - 1 > 0:
        if s.celulas[ry + 1, COLUNAS[rx - 1] ] == RATOICON:
          v_ratos += 6 / 5

      if rx + 1 < LINHAS:
        if s.celulas[ry + 1, COLUNAS[rx + 1] ] == RATOICON:
          v_ratos += 6 / 5

      
      # verifica se há obstáculo entre o gato e o rato em (y)        
      obstaculo = False
      origem, destino = (gy, ry) if gy < ry else (ry, gy)
      
      for yy in range(origem + 1, destino):
        if s.celulas[yy, rx] != None:
          obstaculo = True

      if not obstaculo:
        v_gatos += 1
      
      else:
        v_gatos += 2

    # Caso2: movimento horizontal (x)
    elif gx == rx:
      # se tem um rato (y + 1) ( x - 1) ou ( x + 2)
      if rx - 1 > 0 :
        if s.celulas[ry + 1, COLUNAS[rx - 1] ] == RATOICON:
          v_ratos += 6 / 5

      if rx + 1 < LINHAS:
        if s.celulas[ry + 1, COLUNAS[rx + 1] ] == RATOICON:
          v_ratos += 6 / 5
      
      # verifica se há obstáculo entre o gato e o rato em (y)                
      obstaculo = False
      origem, destino = (gx, rx) if gx < rx else (rx, gx)
      
      for xx in range(origem + 1, destino):
        if celulas[ ry, COLUNAS[xx]] != None:
          obstaculo = True
        
      if not obstaculo:
        v_gatos += 1
      else: 
        v_gatos += 2
      
    
    else:
      v_gatos += 2

    # ----------  RATO ----------------- #
    # Categoria do estado: em quantas rodadas rato ganha ?
    # tem que considerar o obstáculo ?
    v_ratos +=  sqrt((rx-rx)**2) + ((ry-1)**2)

  # testar peso para ratos agrupados
  # se um rato possui defesa então ele tem mais chances de ganhar

  
  #EVAL(s) = peso(r)*(nTurnos.PRatoGanhar) - peso(g)*(nTurnos.GatoGanhar)
  
  # Peso: 1 vitoria do rato equivale a |ratos.restantes| capturas do gato
  wG = (1/ratos_restantes) * .6
  wR = (ratos_restantes) * .1
  

  evals = wR*v_ratos - wG*v_gatos
  
  return evals


#===============================================================================
 
  #============================================================================= 
  # HEURISTICA
  #=============================================================================
  def heuristica(self, s):
    vantagem = 0
    desvantagem = 0

    gy, _gx = s.gato.pos
    gx = s.Cols.index(_gx)

    """
    
    ry, _rx = s.ratos.pos[idx]
    rx = s.Cols.index(_rx)
    yy, _xx = s.ratos.pos[ii]
    xx = s.Cols.index(_xx)

    Caracteristicas de estado:
    
    w(i)*f(i): Ratos em "escadinha tem maior chance"

    |rA|_____________|rH|
      |rB|__________|rG|
        |rC|_______|rF|

    -------------------------------------------
    f(1) Esq  :: w(1) |Esq| * .25
    f(2) Dir  :: w(2) |Dir| * .25
    -------------------------------------------
    
    """

    fesq = []
    w_esq = .25
    
    fdir = []
    w_dir = .25

    dist_esq = []
    dist_dir = []

    dist_gato = []

    g_captura = 0

    for idx in range(s.ratos.n):
      ry, _rx = s.ratos.pos[idx]
      rx = s.Cols.index(_rx)
      
      # verifica ratos na diagonal
      if _rx == 'A' or _rx == 'B' or _rx == 'C':
        
        fesq.append((ry, rx))
        
        d = sqrt((rx-rx)**2) + ((ry-1)**2)

        if  gy != ry:
          d = d * 1.5

        dist_esq.append(d)

      
      elif _rx == 'F' or _rx == 'G' or _rx == 'H':
        
        fdir.append((ry, rx))
        
        d = sqrt((rx-rx)**2) + ((ry-1)**2)
        
        if  gy != ry:
          d * 1.5

        dist_esq.append(d)
        
        


      # verifica movimento de captura p gato
      # if gy == ry or gx == rx:        
      #   g_captura += 1

      if gy == ry:
        if rx - 1 > 0 and s.celulas[ ry + 1, COLUNAS[rx - 1] ]:
          g_captura -= 3
        
        elif rx + 1 < 8 and s.celulas[ ry + 1, COLUNAS[rx + 1] ]:
          g_captura -= 3

        else:
          g_captura += 1
      

      
      
      
      
      # f(3) distancia dos ratos do gato
      dist_gato.append(sqrt((rx-gx)**2) + ((ry-gx)**2))
  


    # Obtém valor de w(i) para os grupos
    ya, yb, yc, yf, yg, yh = 0,0,0,0,0,0
    

    for y in range(LINHAS):
      # ESQ ----------------
      if (y, 'A') in fesq:
        ya = y
      if (y, 'B') in fesq:
        yb = y
      if (y, 'C') in fesq:
        yc = y

      # DIR ----------------
      if (y, 'F') in fesq:
        yf = y
      if (y, 'G') in fesq:
        yg = y
      if (y, 'H') in fesq:
        yh = y

    # obter w(esq)
    if ya - 1 == yb or ya + 1 == yb :
      w_esq += .7 
    if yb - 1 == yc or yb + 1 == yc:
      w_esq += .7 

    # obter w(esq)
    if yh - 1 == yg or yh + 1 == yg:
      w_dir += .7
    if yg - 1 == yf or yg + 1 == yf :
      w_dir += .7

    esq_avg = reduce(lambda a, b: a + b, dist_esq) if len(dist_esq) > 0 else 0
    dir_avg = reduce(lambda a, b: a + b, dist_dir) if len(dist_dir) > 0 else 0
    md_gato = reduce(lambda a, b: a + b, dist_gato) / s.ratos.n  # 
    esq_avg = max(dist_esq) if len(dist_esq) > 0 else -1
    dir_avg = max(dist_dir) if len(dist_dir) > 0 else -1

    Evals = (w_esq*esq_avg + w_dir*dir_avg) - (g_captura*s.ratos.n)