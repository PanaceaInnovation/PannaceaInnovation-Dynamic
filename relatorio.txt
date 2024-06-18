PANACEA INNOVATION

Integrantes:

Felipe de Campos Mello Arnus - RM 550923
João Pedro Oliveira Chambrone - RM 97857
João Pedro de Souza Vieira - RM 99805
Leticia Cristina Gandarez Resina - RM 98069
Vitor Hugo Gonçalves Rodrigues - RM 97758


OBS: PARA RODAR O JOGO CORRETAMENTE EXECUTE 'pip install -r requirements.txt' NO TERMINAL;

DESAFIOS CUMPRIDOS

OBS: TODOS OS DESAFIOS SE ENCONTRAM NO MESMO ARQUIVO "jogo.py";

- Pedra: desenhar um retângulo, de outra cor, que não permite a passagem do jogador; 

Este desafio foi cumprido. Como podemos ver no código, são desenhados retângulos cinzas dos quais não permitem a passagem do jogador.

- Dar suporte a múltiplas 'pedras';

Este desafio também foi cumprido, como se pode observar na execução do jogo. Adicionamos vários retângulos cinzas ("Pedras") espalhados pela tela.

- Labirinto: usando múltiplas 'pedras', desenhar um labirinto 'na mão', de forma que o jogador, iniciando no centro do tabuleiro, tenha que atingir a borda;

Este desafio foi cumprido. Posicionamos as pedras de forma com que formam um "labirinto" o que exige do jogador que ele desvie e tente sair de perto das pedras para que ele possa 
"comer" as comidas.

- Exibir, no cmd do Windows, uma contagem de quantos 'pontos' o jogador fez, quantos quadradinhos 'comeu';

Este desafio foi cumprido. A puntuação, a medida que o jogador come as comidas, é exibida e atualizada no terminal ou cmd. A pontuação final também é exibida.

- Exibir na tela do jogo a pontuação;

Este desafio foi cumprido. A pontuação é exibida na tela, e atualizada a medida que o jogador come os quadradinhos.

- Fazer o jogador 'crescer' quando ele come um quadradinho;

Este desafio foi cumprido. O jogador cresce gradualmente, a medida que come as comidas. A dificuldade do jogo vai aumentando, pois se torna mais difícil passar pelos obstáculos.

- Permitir 'wrap around': um jogador que 'sai' da tela à esquerda volta do lado direito. O mesmo acontece indo para a esquerda, para a direita, para cima ou para baixo;

Esta funcionalidade foi implementada. O jogador quando sai da tela pelo lado esquerdo e volta pelo direita, e vice e versa. O mesmo acontece para cima e para baixo.

RESUMO DO FUNCIONAMENTO E OUTRAS IMPLEMENTAÇÕES

        A Panacea Innovation desenvolveu um minigame que contém todos os desafios propostos pelo professor implementados. Além dos desafios implementados, 
através de pesquisa, foi possível adicionar algumas outras funcionalidades, que deixam o jogo mais interessante e divertido. Adicionamos um tempo limite de 40s, 
do qual torna o jogo mais desafiador. Este tempo é exibido na tela ao lado da pontuação, e é atualizado conforme os segundos vão passando. Além do tempo limite, 
definimos uma meta da qual o jogador tem que atingir para poder vencer o jogo. Ela também é exibida ne tela do jogo. Caso ele consiga atingir essa meta dentro do 
tempo limite (50 pontos), uma mensagem de vitória é exibida no terminal ou cmd. Caso contrário, uma mensagem de derrota também será exibida. Além dessas implementações,
personalizamos cores, e colocamos o nome de nossa solução dentro do jogador. O código base, é o código do capítulo 19 do professor Al Sweigar, que foi modificado e personalizado
com tudo que citamos. Vale ressaltar que o código está comentado, para que facilite o seu entendimento. Para rodar perfeitamente, basta instalar o arquivo requirements.txt, como
ja foi destacado acima.
