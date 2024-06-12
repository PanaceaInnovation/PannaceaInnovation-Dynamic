# jogo.py
import pygame
import sys
import random
from pygame.locals import *

# Inicialização do Pygame
pygame.init()
mainClock = pygame.time.Clock()

# Definição das dimensões da janela
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Jogo de Colisões e Labirinto')

# Definição das cores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Contador de comida e configurações relacionadas à comida
foodCounter = 0
NEWFOOD = 40
FOODSIZE = 20

# Definição do retângulo do jogador
player = pygame.Rect(300, 300, 50, 50)
player_color = BLACK

# Lista que armazenará os retângulos da comida
foods = [pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE),
                     random.randint(0, WINDOWHEIGHT - FOODSIZE),
                     FOODSIZE, FOODSIZE) for _ in range(20)]

# Lista de 'pedras' (obstáculos)
rocks = [
    pygame.Rect(100, 100, 100, 50),
    pygame.Rect(250, 100, 50, 200),
    pygame.Rect(400, 100, 100, 50),
    pygame.Rect(100, 300, 50, 200),
    pygame.Rect(400, 300, 50, 200),
    pygame.Rect(250, 400, 200, 50),
    pygame.Rect(100, 500, 400, 50)
]

# Variáveis de movimento do jogador
moveLeft = False
moveRight = False
moveUp = False
moveDown = False

# Velocidade de movimento do jogador
MOVESPEED = 6

# Contador de pontuação
score = 0

# Fonte para exibição de texto na tela
font = pygame.font.SysFont(None, 36)

# Função para verificar colisão com pedras
def check_collision_with_rocks(player, rocks):
    for rock in rocks:
        if player.colliderect(rock):
            return True
    return False

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

    # Movimento do jogador
    if moveDown:
        player.top += MOVESPEED
    if moveUp:
        player.top -= MOVESPEED
    if moveLeft:
        player.left -= MOVESPEED
    if moveRight:
        player.right += MOVESPEED

    # Implementação do 'wrap around'
    if player.top < 0:
        player.top = WINDOWHEIGHT - player.height
    if player.bottom > WINDOWHEIGHT:
        player.top = 0
    if player.left < 0:
        player.left = WINDOWWIDTH - player.width
    if player.right > WINDOWWIDTH:
        player.left = 0

    # Verifica colisão com pedras e desfaz movimento se necessário
    if check_collision_with_rocks(player, rocks):
        if moveDown:
            player.top -= MOVESPEED
        if moveUp:
            player.top += MOVESPEED
        if moveLeft:
            player.left += MOVESPEED
        if moveRight:
            player.right -= MOVESPEED

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

    # Desenha o jogador
    pygame.draw.rect(windowSurface, player_color, player)

    # Verifica colisões entre o jogador e a comida e remove a comida se houver colisão
    for food in foods[:]:
        if player.colliderect(food):
            foods.remove(food)
            score += 1
            player.inflate_ip(5, 5)  # Aumenta o tamanho do jogador
            print(f"Pontuação: {score}")

    # Desenha a comida
    for food in foods:
        pygame.draw.rect(windowSurface, GREEN, food)

    # Desenha as pedras
    for rock in rocks:
        pygame.draw.rect(windowSurface, RED, rock)

    # Exibe a pontuação na tela do jogo
    score_text = font.render(f'Pontuação: {score}', True, BLACK)
    windowSurface.blit(score_text, (10, 10))

    # Atualiza a tela
    pygame.display.update()
    # Limita a taxa de quadros por segundo
    mainClock.tick(40)


