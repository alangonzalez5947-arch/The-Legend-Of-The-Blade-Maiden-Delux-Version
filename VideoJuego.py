import pygame
from Personaje import personaje 
import Constantes #importar las constantes del juego
from Enemigo import enemigo
import random


pygame.font.init()


ventana = pygame.display.set_mode((Constantes.ANCHO_VENTANA, Constantes.ALTO_VENTANA), pygame.FULLSCREEN)


pantalla_ancho = ventana.get_width()
pantalla_alto = ventana.get_height()

fondo = pygame.image.load("Assets//Images//Background//Background_image.png")
fondo = pygame.transform.scale(fondo, (Constantes.ANCHO_VENTANA, Constantes.ALTO_VENTANA))
    

#crear el suelo 
suelo_altura = 126

  #grosor del suelo
suelo_y = pantalla_alto - suelo_altura
suelo = pygame.Rect(0, suelo_y, pantalla_ancho, suelo_altura)


pygame.display.set_caption("The Legend of the Blade Maiden")

def mostrar_game_over(ventana):
    fuente = pygame.font.SysFont("Arial", 80, bold=True)
    texto = fuente.render("Game Over", True, (255,0,0))

    #cerrar en pantalla
    rect = texto.get_rect(center=(ventana.get_width()//2, ventana.get_height()//2))
    ventana.blit(texto, rect)
    pygame.display.update()


def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, size = (w*scale, h*scale))
    return nueva_imagen

animaciones_walk = []
for i in range(7):
    img = pygame.image.load(f"Assets//Images//Characters//Player//Walking_{i}.png")
    img = escalar_img(img, Constantes.SCALA_PERSONAJE)
    animaciones_walk.append(img)

animaciones_idle = []
for i in range(1):
    img = pygame.image.load(f"Assets//Images//Characters//Player//Idle//Idle_KG_0.png")
    img = escalar_img(img, Constantes.SCALA_PERSONAJE)
    animaciones_idle.append(img)

animaciones_jump = []
for i in range(6):
    img = pygame.image.load(f"Assets//Images//Characters//Player//Jump//Jump_KG_{i}.png")
    img = escalar_img(img, Constantes.SCALA_PERSONAJE)
    animaciones_jump.append(img)

animaciones_crouch = []
for i in range(3):
    img = pygame.image.load(f"Assets//Images//Characters//Player//Crouching//Crouching_KG_{i}.png")
    img = escalar_img(img, Constantes.SCALA_PERSONAJE)
    animaciones_crouch.append(img)

animaciones_attack = []
for i in range(6):
    img = pygame.image.load(f"Assets//Images//Characters//Player//Ataque principal//Attack_KG_{i}.png")
    img = escalar_img(img, Constantes.SCALA_PERSONAJE)
    animaciones_attack.append(img)

animaciones_dead = []
for i in range(6):
    img = pygame.image.load(f"Assets//Images//Characters//Player//Die//Dying_KG_{i}.png")
    img = escalar_img(img, Constantes.SCALA_PERSONAJE)
    animaciones_dead.append(img)

jugador = personaje(500, 500, animaciones_idle, animaciones_walk, animaciones_jump, animaciones_crouch, animaciones_attack, animaciones_dead)

enemigos = []



#definir las variables de movimiento del jugador
mover_izquierda = False
mover_derecha = False

#Controla los Frames
reloj = pygame.time.Clock()
run = True

#spawn enemigo
spawn_rate = 4500 # 4.5 segundos
ultimo_spawn = 0



while run == True:


    #Que vaya a 60 FPS
    reloj.tick(Constantes.FPS)

    #calcular dt
    dt = reloj.get_time() / 1000
    
    ventana.blit(fondo, (0,0))


    tiempo_actual = pygame.time.get_ticks()

    if jugador.vivo and tiempo_actual - ultimo_spawn >= spawn_rate:
        x = random.randint(100, 700)
        y = 500
        enemigos.append(enemigo (x, y, escala = 5))
        ultimo_spawn = tiempo_actual
    

    #Calcular movimiento de jugador
    delta_x = 0


    if mover_derecha == True:
        delta_x = Constantes.VELOCIDAD
    if mover_izquierda == True:
        delta_x = -Constantes.VELOCIDAD


    
    keys = pygame.key.get_pressed()
    jugador.agachado = keys[pygame.K_s]


    

      #mover al jugador
    jugador.movimiento(delta_x)
    jugador.update(enemigos)
    jugador.dibujar(ventana)

    if not jugador.vivo:

        if not jugador.animacion_muerte_terminada:
            jugador.update([])
            jugador.dibujar(ventana)
            pygame.display.update()
            continue


        mostrar_game_over(ventana)
        pygame.time.delay(6000)
        run = False
        continue

    


    #actualiza enemigos
    for e in enemigos:
        e.update(jugador, dt)
        e.dibujar(ventana)

    #eliminar enemigos
    enemigos = [e for e in enemigos if not e.animacion_muerte_terminada]

    #def dibujar_hitboxes(ventana, enemigo, jugador):
        # Dibujar rect del enemigo (verde)
        #pygame.draw.rect(ventana, (0,255,0), enemigo.rect, 2)

         # Dibujar rect del jugador (azul)
        #pygame.draw.rect(ventana, (0,128,255), jugador.rect, 2)

        # Dibujar hitbox de ataque si existe (rojo)
        #hitbox = enemigo.get_hitbox_ataque()
        #if hitbox:
           # pygame.draw.rect(ventana, (255,0,0), hitbox, 2)



    #sssssssdibujar_hitboxes(ventana, enemigo, jugador)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
               mover_derecha = True

            if event.key == pygame.K_SPACE:
                jugador.saltar()

            if event.key == pygame.K_j:
                jugador.atacar()
            
            if event.key == pygame.K_ESCAPE:
                run = False

            
        #Para cuando se suelte la tecla 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_d:
               mover_derecha = False

            

    pygame.draw.rect(ventana, (120, 70, 20), suelo)
    pygame.display.update()

pygame.quit()

