# CSI701TP: Algoritmo MiniMax em agentes inteligentes

## CSI701 - Inteligência Artificial :: 2022.1

Este projeto implementa uma versão do jogo de tabuleiro "Gato e Ratos". Onde o gato é controlado por um jogador humano e os ratos são controlados por um agente inteligente. 

O Algoritmo de busca Minimax aplicado ao contexto dos agentes inteligentes tem como objetivo determinar a melhor jogada em um jogo de soma zero, considerando as possíveis ações do agente e do oponente, visando minimizar as perdas máximas.

### Grupo:

 - Kassio Rodrigues Ferreira
 - Pedro Alexandre Souto

#### Executando o jogo:

O único requisito é ter o python 3.9^ instalado. 

No diretório raiz basta executar o comando 

```
$ python main.py
```

---
### O Jogo de Gato e Ratos:

#### Objetivo do gato

 - capturar todos os ratos.

#### Objetivo dos ratos:

 - chegar um dos ratos ao outro lado do tabuleiro;
 - ou capturar o gato
 - assim que **um** rato chegar ao final do tabuleiro, os ratos vencem o jogo (_mesmo que o gato possa capturar o rato da chegada na proxima jogada_).

#### Regras para os Ratos:

 1. Na sua vez, o jogador com os ratos pode mover apenas um de seus ratos;
 2. O rato só pode mover-se para frente;
 3. O rato avança uma casa por vez;
 4. Apenas em seu primeiro movimento, cada rato pode escolher entre avançar uma ou duas casas;
 5. O rato só pode capturar na diagonal;
 6. O rato não pode mover-se para trás, nem capturar para trás.

#### Regras de movimento para o Gato

 1. O gato pode mover-se para frente, trás e lados, e pode capturar os ratos nestas direções;
 2. O gato não pode mover-se nem capturar na diagonal;
 3. O gato pode mover-se quantas casas quiser, desde que o caminho **esteja livre**;
 4. Quando o gato captura um rato, passa a ocupar a casa em que o rato estava;
 5. O gato só pode capturar um rato por jogada.


  


  
