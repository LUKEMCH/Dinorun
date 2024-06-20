import pygame
import random
import sys
import matplotlib.pyplot as plt

# Inicialização do Pygame
pygame.init()

# Configurações da tela
screen_width = 1500
screen_height = 680
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo do Dinossauro") 

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

# Carregar imagens
dino_image = pygame.image.load('dino.png')
obstacle_image = pygame.image.load('obstacle.png')
background_image = pygame.image.load('background.png')

# Redimensionar o obstáculo
obstacle_image = pygame.transform.scale(obstacle_image, (120, 120))  # Novo tamanho do obstáculo

# Configurações do dinossauro
dino_width = dino_image.get_width()
dino_height = dino_image.get_height()
dino_x = 50
dino_y = screen_height - dino_height - 20
dino_vel_y = 0
gravity = 1
jump_strength = -15
is_jumping = False

# Configurações do obstáculo
obstacle_width = obstacle_image.get_width()
obstacle_height = obstacle_image.get_height()
obstacle_x = screen_width
obstacle_y = screen_height - obstacle_height - 20
obstacle_speed = 10  # Velocidade em metros por segundo

# Configurações do fundo
background_width = background_image.get_width()
background_height = background_image.get_height()
background_x1 = 0
background_x2 = background_width
background_speed = 5  # Velocidade em metros por segundo

# Velocidade do jogo em metros por segundo
game_speed = 10
speed_multiplier = 1  # Multiplicador de velocidade inicial

# Fonte para texto
font = pygame.font.Font(None, 32)  # Aumentando o tamanho da fonte para 32

# Função para desenhar o dinossauro
def draw_dino(x, y):
    screen.blit(dino_image, (x, y))

# Função para desenhar o obstáculo
def draw_obstacle(x, y):
    screen.blit(obstacle_image, (x, y))

# Função para desenhar informações na tela
def draw_info(time_elapsed, speed, distance, average_speed, acceleration):
    info_text = font.render(f'Tempo: {time_elapsed//1000}s | Velocidade: {speed}x | Distância: {distance} m | Velocidade Média: {average_speed} m/s | Aceleração: {acceleration} px/ms²', True, BLACK)
    screen.blit(info_text, (10, 10))

# Função principal do jogo
def game_loop():
    global dino_y, dino_vel_y, is_jumping, obstacle_x, background_x1, background_x2, game_speed, speed_multiplier

    clock = pygame.time.Clock()
    running = True
    start_time = pygame.time.get_ticks()
    elapsed_time = 0
    distance = 0
    average_speed = 0

    # Dados para plotagem
    time_data = []
    position_data = []
    velocity_data = []
    acceleration_data = []

    # Botão para aumentar a velocidade
    button_width = 150
    button_height = 50
    button_x = screen_width - button_width - 10
    button_y = screen_height - button_height - 10

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping:
                    dino_vel_y = jump_strength
                    is_jumping = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    speed_multiplier += 1

        # Movimento do dinossauro
        dino_y += dino_vel_y
        if is_jumping:
            dino_vel_y += gravity

        if dino_y >= screen_height - dino_height - 20:
            dino_y = screen_height - dino_height - 20
            is_jumping = False
            dino_vel_y = 0

        # Movimento do obstáculo
        obstacle_x -= obstacle_speed * game_speed * speed_multiplier / 10  # Ajuste da velocidade com base no game_speed e no multiplicador de velocidade
        if obstacle_x < 0:
            obstacle_x = screen_width + random.randint(0, 300)

        # Movimento do fundo
        background_x1 -= background_speed * game_speed * speed_multiplier / 10  # Ajuste da velocidade com base no game_speed e no multiplicador de velocidade
        background_x2 -= background_speed * game_speed * speed_multiplier / 10  # Ajuste da velocidade com base no game_speed e no multiplicador de velocidade
        
        if background_x1 <= -background_width:
            background_x1 = background_width + background_x2
        if background_x2 <= -background_width:
            background_x2 = background_width + background_x1

        # Atualização do tempo e distância
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        distance += obstacle_speed * game_speed * speed_multiplier / 10  # Ajuste da distância com base no game_speed e no multiplicador de velocidade

        # Atualização da velocidade média
        if elapsed_time > 0:
            average_speed = distance / elapsed_time * 1000

        # Aceleração baseada no multiplicador de velocidade
        acceleration = 0.1 * speed_multiplier  # Ajuste o fator de aceleração conforme necessário

        # Captura de dados
        time_data.append(current_time - start_time)
        position_data.append(dino_y)
        velocity_data.append(dino_vel_y)
        acceleration_data.append(acceleration)

        # Desenho na tela
        screen.fill(WHITE)
        screen.blit(background_image, (background_x1, 0))
        screen.blit(background_image, (background_x2, 0))
        draw_dino(dino_x, dino_y)
        draw_obstacle(obstacle_x, obstacle_y)
        draw_info(elapsed_time, speed_multiplier, round(distance, 1), round(average_speed, 1), round(acceleration, 1))

        # Desenho do botão
        pygame.draw.rect(screen, GRAY, (button_x, button_y, button_width, button_height))
        button_text = font.render(f'Turbo', True, BLACK)
        screen.blit(button_text, (button_x + 10, button_y + 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

    # Plotagem dos gráficos
    plt.figure(figsize=(12, 6))

    # Gráfico de Posição vs Tempo
    plt.subplot(2, 2, 1)
    plt.plot(time_data, position_data, color='blue')
    plt.xlabel('Tempo (ms)')
    plt.ylabel('Posição (pixels)')
    plt.title('Posição vs Tempo')

    # Gráfico de Velocidade vs Tempo
    plt.subplot(2, 2, 2)
    plt.plot(time_data, velocity_data, color='green')
    plt.xlabel('Tempo (ms)')
    plt.ylabel('Velocidade (pixels/ms)')
    plt.title('Velocidade vs Tempo')

    # Gráfico de Aceleração vs Tempo
    plt.subplot(2, 2, 3)
    plt.plot(time_data, acceleration_data, color='red')
    plt.xlabel('Tempo (ms)')
    plt.ylabel('Aceleração (pixels/ms²)')
    plt.title('Aceleração vs Tempo')

    plt.tight_layout()
    plt.show()
    sys.exit()

# Tela inicial
def start_screen():
    screen.fill(WHITE)
    title_text = font.render('Jogo do Dinossauro', True, BLACK)
    instruction_text = font.render('Pressione Espaço para Iniciar', True, BLACK)
    screen.blit(title_text, (screen_width//2 - title_text.get_width()//2, screen_height//2 - 50))
    screen.blit(instruction_text, (screen_width//2 - instruction_text.get_width()//2, screen_height//2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Iniciar o jogo
start_screen()
game_loop()
