import pygame, sys, random
from pygame.locals import *

#ATENÇÃO! SÓ FUNCIONARÁ DEPOIS QUE A BIBLIOTECA PYGAME ESTIVER INSTALADA  ('pip install pygame' no terminal)

#Basicamente o jogo consiste só em fazer com que quando o player passe pelo quadradinho verde (as comidas), elas sumam. Precisamos implementar obstáculos e fazer algumas modificações que o professor pede.

# Inicialização do Pygame
pygame.init()
mainClock = pygame.time.Clock()

# Definição das dimensões da janela
WINDOWWIDTH = 400
WINDOWHEIGHT = 400
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Collision Detection')

# Definição das cores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Contador de comida e configurações relacionadas à comida
foodCounter = 0
NEWFOOD = 40
FOODSIZE = 20

# Definição do retângulo do jogador
player = pygame.Rect(300, 100, 50, 50)

# Lista que armazenará os retângulos da comida
foods = [pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE),
                     random.randint(0, WINDOWHEIGHT - FOODSIZE),
                     FOODSIZE, FOODSIZE) for _ in range(20)]

# Variáveis de movimento do jogador
moveLeft = False
moveRight = False
moveUp = False
moveDown = False

# Velocidade de movimento do jogador
MOVESPEED = 6

# Loop principal do jogo
while True:
    # Eventos do Pygame
    for event in pygame.event.get():
        # Evento de fechar a janela
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # Eventos de pressionar teclas
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_a:
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == K_d:
                moveLeft = False
                moveRight = True
            if event.key == K_UP or event.key == K_w:
                moveDown = False
                moveUp = True
            if event.key == K_DOWN or event.key == K_s:
                moveUp = False
                moveDown = True
        # Eventos de soltar teclas
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == K_a:
                moveLeft = False
            if event.key == K_RIGHT or event.key == K_d:
                moveRight = False
            if event.key == K_UP or event.key == K_w:
                moveUp = False
            if event.key == K_DOWN or event.key == K_s:
                moveDown = False
            if event.key == K_x:
                player.top = random.randint(0, WINDOWHEIGHT - player.height)
                player.left = random.randint(0, WINDOWWIDTH - player.width)
        # Eventos de clique do mouse
        if event.type == MOUSEBUTTONUP:
            foods.append(pygame.Rect(event.pos[0], event.pos[1], FOODSIZE, FOODSIZE))

    # Contagem de comida
    foodCounter += 1
    # Adiciona nova comida após um determinado número de frames
    if foodCounter >= NEWFOOD:
        foodCounter = 0
        foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE),
                                 random.randint(0, WINDOWHEIGHT - FOODSIZE),
                                 FOODSIZE, FOODSIZE))

    # Limpa a tela
    windowSurface.fill(WHITE)

    # Movimento do jogador
    if moveDown and player.bottom < WINDOWHEIGHT:
        player.top += MOVESPEED
    if moveUp and player.top > 0:
        player.top -= MOVESPEED
    if moveLeft and player.left > 0:
        player.left -= MOVESPEED
    if moveRight and player.right < WINDOWWIDTH:
        player.right += MOVESPEED

    # Desenha o jogador
    pygame.draw.rect(windowSurface, BLACK, player)

    # Verifica colisões entre o jogador e a comida e remove a comida se houver colisão
    for food in foods[:]:
        if player.colliderect(food):
            foods.remove(food)

    # Desenha a comida
    for food in foods:
        pygame.draw.rect(windowSurface, GREEN, food)

    # Atualiza a tela
    pygame.display.update()
    # Limita a taxa de quadros por segundo
    mainClock.tick(40)
