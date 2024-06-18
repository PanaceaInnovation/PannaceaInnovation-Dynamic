import pygame
import sys
import random
import time
from pygame.locals import *

# Inicialização do Pygame
pygame.init()
mainClock = pygame.time.Clock()

# Definição das dimensões da janela
WINDOWWIDTH = 700
WINDOWHEIGHT = 700
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('PANACEA INNOVATION Minigame')

# Definição das cores
BLACK = (0, 0, 0)
GREEN = (80, 200, 120)  # Verde esmeralda para o jogador
WHITE = (255, 255, 255)
RED = (255, 0, 0)       # Vermelho para a comida
GRAY = (169, 169, 169)  # Cinza para as pedras


# Contador de comida e configurações relacionadas à comida
foodCounter = 0
NEWFOOD = 40
FOODSIZE = 30  # Tamanho da comida

# Definições do jogador
playerSize = 45  # Tamanho inicial do jogador
playerRect = pygame.Rect(300, 300, playerSize, playerSize)

# Fonte para o texto dentro do jogador
playerFont = pygame.font.SysFont(None, 11)

# Lista que armazenará os retângulos da comida
foods = [pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE),
                     random.randint(0, WINDOWHEIGHT - FOODSIZE),
                     FOODSIZE, FOODSIZE) for _ in range(20)]

# Lista de 'pedras' 
rocks = [
    pygame.Rect(50, 50, 100, 20),
    pygame.Rect(250, 150, 20, 140),
    pygame.Rect(450, 80, 100, 20),
    pygame.Rect(150, 350, 20, 140),
    pygame.Rect(550, 280, 20, 140),
    pygame.Rect(200, 500, 140, 20),
    pygame.Rect(500, 450, 140, 20)
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
small_font = pygame.font.SysFont(None, 18)  

# Variável para o tempo limite do jogo (em segundos)
TIME_LIMIT = 40  
start_time = time.time()

# Função para verificar colisão com pedras
def check_collision_with_rocks(player, rocks):
    for rock in rocks:
        if player.colliderect(rock):
            return True
    return False

# Função para verificar se o jogador ganhou ou perdeu
def check_game_result(score):
    if score >= 50:
        return "Parabéns! Você venceu!"
    else:
        return "Você não alcançou 50 pontos. Tente novamente!"

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

    # Verifica o tempo decorrido e termina o jogo se exceder o limite de tempo
    elapsed_time = time.time() - start_time
    time_remaining = max(0, TIME_LIMIT - int(elapsed_time))  # Calcula o tempo restante em segundos

    # Verifica se o tempo acabou
    if elapsed_time >= TIME_LIMIT:
        result_message = check_game_result(score)
        print(f'Tempo esgotado! {result_message} Pontuação final: {score}')
        pygame.quit()
        sys.exit()

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

    # Limpar a tela com uma cor de fundo
    windowSurface.fill(BLACK)

    # Desenha o jogador
    pygame.draw.rect(windowSurface, GREEN, playerRect)

    # Adiciona texto dentro do jogador (com quebra de linha)
    line1 = playerFont.render("PANACEA", True, WHITE)
    line2 = playerFont.render("INNOVATION", True, WHITE)
    
    textRect1 = line1.get_rect(midtop=(playerRect.centerx, playerRect.top + 5))
    textRect2 = line2.get_rect(midtop=(playerRect.centerx, playerRect.top + 15))
    
    windowSurface.blit(line1, textRect1)
    windowSurface.blit(line2, textRect2)

    # Exibe o tempo restante na tela
    time_text = font.render(f'Tempo restante: {time_remaining} s', True, WHITE)
    windowSurface.blit(time_text, (10, 10))

    # Exibe a pontuação na tela do jogo
    score_text = font.render(f'Pontuação: {score}', True, WHITE)
    score_text_rect = score_text.get_rect(topright=(WINDOWWIDTH - 10, 10))
    windowSurface.blit(score_text, score_text_rect)

    # Exibe o texto da meta
    win_condition_text = small_font.render('TENTE FAZER 50 PONTOS PARA VENCER!', True, WHITE)
    win_condition_rect = win_condition_text.get_rect(midtop=(WINDOWWIDTH // 1.8, 40))
    windowSurface.blit(win_condition_text, win_condition_rect)

    # Verifica colisões entre o jogador e a comida e remove a comida se houver colisão
    for food in foods[:]:
        if playerRect.colliderect(food):
            foods.remove(food)
            score += 1
            # Aumenta o tamanho do jogador
            playerRect.inflate_ip(2, 2)  # Aumenta o tamanho do retângulo em 2 pixels em cada direção
            print(f"Pontuação: {score}")

    # Desenha a comida
    for food in foods:
        pygame.draw.rect(windowSurface, RED, food)

    # Desenha as pedras
    for rock in rocks:
        pygame.draw.rect(windowSurface, GRAY, rock)

    # Atualiza a tela
    pygame.display.update()
    # Limita a taxa de quadros por segundo
    mainClock.tick(40)



