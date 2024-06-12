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

# Carregar a imagem do jogador
playerImage = pygame.image.load('img/170.png')  # Certifique-se de que a imagem está no mesmo diretório ou forneça o caminho completo
playerImage = pygame.transform.scale(playerImage, (50, 50))  # Redimensionar a imagem se necessário
playerRect = playerImage.get_rect()
playerRect.topleft = (300, 300)

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
                playerRect.top = random.randint(0, WINDOWHEIGHT - playerRect.height)
                playerRect.left = random.randint(0, WINDOWWIDTH - playerRect.width)
        # Eventos de clique do mouse
        if event.type == MOUSEBUTTONUP:
            foods.append(pygame.Rect(event.pos[0], event.pos[1], FOODSIZE, FOODSIZE))

    # Movimento do jogador
    if moveDown:
        playerRect.top += MOVESPEED
    if moveUp:
        playerRect.top -= MOVESPEED
    if moveLeft:
        playerRect.left -= MOVESPEED
    if moveRight:
        playerRect.left += MOVESPEED

    # Implementação do 'wrap around'
    if playerRect.top < 0:
        playerRect.top = WINDOWHEIGHT - playerRect.height
    if playerRect.bottom > WINDOWHEIGHT:
        playerRect.top = 0
    if playerRect.left < 0:
        playerRect.left = WINDOWWIDTH - playerRect.width
    if playerRect.right > WINDOWWIDTH:
        playerRect.left = 0

    # Verifica colisão com pedras e desfaz movimento se necessário
    if check_collision_with_rocks(playerRect, rocks):
        if moveDown:
            playerRect.top -= MOVESPEED
        if moveUp:
            playerRect.top += MOVESPEED
        if moveLeft:
            playerRect.left += MOVESPEED
        if moveRight:
            playerRect.left -= MOVESPEED

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
    windowSurface.blit(playerImage, playerRect)

    # Verifica colisões entre o jogador e a comida e remove a comida se houver colisão
    for food in foods[:]:
        if playerRect.colliderect(food):
            foods.remove(food)
            score += 1
            # Aumenta o tamanho da imagem do jogador
            playerRect.inflate_ip(5, 5)  # Aumenta o tamanho do retângulo
            playerImage = pygame.transform.scale(playerImage, (playerRect.width, playerRect.height))
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

