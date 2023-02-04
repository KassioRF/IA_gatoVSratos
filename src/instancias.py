
"""-----------------------------------------------------------------------------
 Utiliza o padrão Singleton para instanciar os objetos que compõem o jogo
-----------------------------------------------------------------------------"""

from .jogadores import Gato, Ratos
from .tabuleiro import Tabuleiro
from .Ia_ratos import Ia_Ratos

gato = Gato()
ratos = Ratos()
tabuleiro = Tabuleiro()
bot = Ia_Ratos(ratos, gato, tabuleiro)
