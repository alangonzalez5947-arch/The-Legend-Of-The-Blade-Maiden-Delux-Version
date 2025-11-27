import pygame
import time
import math
import Constantes

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Legend of the Blade Maiden")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 50)


# Aqui van los sprites de animación

player_frames = [
    pygame.image.load("Player_Walking_frame1.png").convert_alpha(),
    pygame.image.load("Player_Walking_frame2.png").convert_alpha(),
    pygame.image.load("Player_Walking_frame3.png").convert_alpha(),
    pygame.image.load("Player_Walking_frame4.png").convert_alpha(),
    pygame.image.load("Player_Walking_frame5.png").convert_alpha(),
    pygame.image.load("Player_Walking_frame6.png").convert_alpha(),
    pygame.image.load("Player_Walking_frame7.png").convert_alpha(),
]

enemy_frames = [
    pygame.image.load("Goblin_running_frame1.png").convert_alpha(),
    pygame.image.load("Goblin_running_frame2.png").convert_alpha(),
    pygame.image.load("Goblin_running_frame3.png").convert_alpha(),
    pygame.image.load("Goblin_running_frame4.png").convert_alpha(),
    pygame.image.load("Goblin_running_frame5.png").convert_alpha(),
    pygame.image.load("Goblin_running_frame6.png").convert_alpha(),
    pygame.image.load("Goblin_running_frame7.png").convert_alpha(),
]

# Reescalar
player_frames = [pygame.transform.scale(img, (100, 60)) for img in player_frames]
enemy_frames  = [pygame.transform.scale(img, (180, 180)) for img in enemy_frames]

def loading_screen(duration=3):

    player_pos = [-400, HEIGHT//2]   # empiezan afuera de pantalla
    enemy_pos  = [-200, HEIGHT//2]

    player_speed = 6
    enemy_speed = 6  
    # índices de animación
    player_frame_index = 0
    enemy_frame_index = 0

    ANIMATION_SPEED = 0.15
    player_anim_timer = 0
    enemy_anim_timer = 0

    start_time = time.time()

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        
        # Movimiento lineal a la derecha
        
        player_pos[0] += player_speed
        enemy_pos[0]  += enemy_speed

        
        # Animación del jugador
        
        player_anim_timer += ANIMATION_SPEED
        if player_anim_timer >= 1:
            player_anim_timer = 0
            player_frame_index = (player_frame_index + 1) % len(player_frames)

        
        # Animación del enemigo
        
        enemy_anim_timer += ANIMATION_SPEED
        if enemy_anim_timer >= 1:
            enemy_anim_timer = 0
            enemy_frame_index = (enemy_frame_index + 1) % len(enemy_frames)

        
        # Dibujar sprites
        
        current_player_img = player_frames[player_frame_index]
        current_enemy_img  = enemy_frames[enemy_frame_index]

        screen.blit(current_player_img, (
            player_pos[0] - current_player_img.get_width()//2,
            player_pos[1] - current_player_img.get_height()//2
        ))

        screen.blit(current_enemy_img, (
            enemy_pos[0] - current_enemy_img.get_width()//2,
            enemy_pos[1] - current_enemy_img.get_height()//2
        ))

        
        # Texto
        
        text = font.render("Now loading...", True, BLACK)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT - 80))

        pygame.display.update()
        clock.tick(60)
        if player_pos[0] > WIDTH + 200 and enemy_pos[0] > WIDTH + 200:
            running = False

loading_screen(4)

def main_menu():
    ventana = pygame.display.set_mode((Constantes.ANCHO_VENTANA, Constantes.ALTO_VENTANA))
    running = True
    
    img = pygame.image.load(f"Assets//images//menu_background.jpg").convert()
    sound = pygame.mixer.music.load(f"Assets//Sound//menu_theme.mp3")

    img = pygame.transform.scale(img, (Constantes.ANCHO_VENTANA, Constantes.ALTO_VENTANA))
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)


    title_font = pygame.font.Font(f"Assets//font//foremost//Foremost Regular.ttf", 80)
    option_font = pygame.font.Font(f"Assets//font//foremost//Foremost Regular.ttf", 50)
    exit_font = pygame.font.Font(f"Assets//font//foremost//Foremost Regular.ttf", 50)

    while running:
        screen.fill((30, 30, 30))
        for event in pygame.event.get():
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # ESCAPE to exit
                    pygame.quit()
                    exit()

           
            if event.key == pygame.K_RETURN:  # ENTER to start
                    running = False
                                    
                    import VideoJuego  # Aquí se llamaría al juego principal
                    VideoJuego.iniciar_juego()

        ventana.blit(img, (0, 0))
            
                
        
        title = title_font.render("The legend of the blade maiden", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))

       
        press_enter = option_font.render("Presiona ENTER para iniciar", True, WHITE)
        press_escape = option_font.render("Presiona EXIT para salir", True, WHITE)
        screen.blit(press_enter, (WIDTH//2 - press_enter.get_width()//1.2, 350))
        screen.blit(press_escape, (WIDTH//2 - press_escape.get_width()//1.1, 420))

        pygame.display.update()
        clock.tick(60)

loading_screen(4)
main_menu()


