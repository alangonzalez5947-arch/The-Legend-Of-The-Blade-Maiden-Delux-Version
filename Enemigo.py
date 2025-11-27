import pygame
import Constantes
from enemy_ai import EnemyAI

class enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, escala = 2):
        super().__init__()

        # IA 
        self.ai = EnemyAI(speed = 2, detection_range=250, flee_range=0)

        #----Animaciones--------
        self.animaciones = {
            "idle": [],
            "walk": [],
            "attack": [],
            "dead": []
        }

        self.cargar_animaciones(escala)

        self.estado = "idle"
        self.frame = 0
        self.time_acc = 0
        self.frame_rate = 0.15    #Aqui va la velocidad de la animacion

        self.image = self.animaciones["idle"][0]
        self.rect = self.image.get_rect(center=(x, y))


       #Fisicas
        self.vel_y = 0
        self.gravedad = 0.6
        self.en_suelo = False
        
        #Estado
        self.vida = 100
        self.vivo = True

        self.flip = False
        
        # Guardar posición del jugador
        self.objetivo_x = x
        self.objetivo_y = y

         # Control de daño
        self.atacando = False
        self.puede_dañar = True   # evita golpear muchas veces por frame
        self.cooldown_golpe = 0.0 # segundos entre golpes
        self.tiempo_ultimo_golpe = 0

        self.animacion_muerte_terminada = False

        

    
    
    def cargar_animaciones(self, escala):


        def cargar_lista(ruta, cantidad):
            lista = []
            for i in range(cantidad):
                img = pygame.image.load(ruta.format(i))
                w,h = img.get_width(), img.get_height()
                img = pygame.transform.scale(img, (int(w* escala), int(h * escala)))
                lista.append(img)
            return lista
        
        #Rutas
        self.animaciones["idle"] = cargar_lista("Assets//Images//Characters//Enemies//Idle_enemy//Golem_0_idle.png", 8)
        self.animaciones["walk"] = cargar_lista("Assets//Images//Characters//Enemies//walk_enemy//Golem_{}_walk.png", 10)
        self.animaciones["attack"] = cargar_lista("Assets//Images//Characters//Enemies//Attack_enemy//Golem_{}_attack.png", 11)
        self.animaciones["dead"] = cargar_lista("Assets//Images//Characters//Enemies//Die_enemy//Golem_{}_die.png", 12)

    def animar(self, dt):
        lista = self.animaciones[self.estado]

        self.time_acc += dt
        if self.time_acc >= self.frame_rate:
            self.time_acc = 0
            self.frame += 1

        
            if self.frame >= len(lista):

                # 🔥 Cuando termina animación de ataque → apagar ataque
                if self.estado in ["attack", "walk", "die"]:
                   self.frame = 0

            
                elif self.estado == "dead":
                   self.frame = len(lista) - 1
                   self.animacion_muerte_terminada = True
                   return
                
                else:
                    self.frame = 0
                  
        frame_index = min(self.frame, len(lista) - 1)

        self.image = pygame.transform.flip(lista[frame_index], self.flip, False)



    def aplicar_gravedad(self):

        if not self.vivo:
            return
        
        #aumentar velocidad vertical
        self.vel_y += self.gravedad

        #limitar velocidad maxima
        if self.vel_y > 12:
            self.vel_y = 12
        
        #mover vertical
        self.rect.y += self.vel_y

        #Colision con suelo
        SUELO_Y = Constantes.ALTO_VENTANA - 75

        if self.rect.bottom > SUELO_Y:
            self.rect.bottom = SUELO_Y
            self.vel_y = 0
            self.en_suelo = True
        else:
            self.en_suelo = False

    def get_hitbox_ataque(self):
        if not self.vivo:
            return None
        if not self.atacando:
            return None
        
        ancho = 100
        alto = 145

        hitbox_y = self.rect.centery - 10


        if not self.flip:  # enemigo mirando derecha
            hitbox_x = self.rect.right - 180
        else:  # mirando izquierda
            hitbox_x = self.rect.left - ancho + 180

        return pygame.Rect(hitbox_x, hitbox_y, ancho, alto)

    
    def atacar(self):
        self.estado = "attack"
        self.frame = 0
        self.golpe_realizado = False
        self.atacando = True



    def recibir_daño(self, cantidad):
        if not self.vivo:
            return
        
        self.vida -= cantidad
        print(f"Enemigo recibió {cantidad} de daño. Vida restante: {self.vida}")
        

    #activa el efecto de daño
        self.daño_timer = pygame.time.get_ticks() #tiempo del inicio del efecto de daño
        self.daño_activo = True

        if self.vida <= 0:
            self.vivo = False
            self.estado = "dead"
            self.frame = 0
            print("Enemigo derrotado.")

    def update(self, objetivo, dt):
        
        # guardar posicion real del jugador
        self.objetivo_x = objetivo.rect.centerx
        self.objetivo_y = objetivo.rect.centery

        if not self.vivo:
            self.estado = "dead"
            self.animar(dt)

            if self.frame >= len(self.animaciones["dead"]) - 1:
                self.animacion_muerte_terminada = True
            return
        
        if not objetivo.vivo:
            self.ai.dx = 0
            self.ai.dy = 0
            self.atacando = False
            self.estado = "idle"
            self.animar(dt)
            return
        
        # Voltear sprite según posición del jugador
        if self.objetivo_x < self.rect.centerx:
            self.flip = True       # mira a la izquierda
        else:
            self.flip = False 
        
       
        self.aplicar_gravedad()

        #ia movimiento
        if not self.atacando:
            self.ai.update(self, (self.objetivo_x, self.objetivo_y))
        else:
            self.ai.dx = 0
            self.ai.dy = 0

            
        # Si está cerca del jugador → atacar automáticamente
        dist = abs(self.rect.centerx - objetivo.rect.centerx)

        if dist < 120 and not self.atacando and objetivo.vivo:
            self.atacar()

        #Estados
        if self.atacando:
            self.estado = "attack"
        elif getattr(self.ai, "dx" , 0) != 0:
            self.estado = "walk"
        else:
            self.estado = "idle"

        

        self.animar(dt)

        # Sistema de daño al jugador
        if self.estado == "attack" and self.vivo and objetivo.vivo:
          hitbox = self.get_hitbox_ataque()
          frame_golpe = 7

        
            
          
             
          if hitbox and int(self.frame) == frame_golpe and not self.golpe_realizado:
                if objetivo.rect.colliderect(hitbox):
                    objetivo.recibir_daño(5)
                    print("🔥 GOLPE REAL APLICADO")
                self.golpe_realizado = True

        lista_actual = self.animaciones[self.estado]
        if int(self.frame) >= len(lista_actual) - 1 and self.estado == "attack":
            self.atacando = False
            self.estado = "idle"
            self.frame = 0

        
               

            
                  


    def dibujar(self, ventana):
            imagen = self.image #imagen normal
            
            # si esta en efecto de daño
            if getattr(self, "daño_activo", False):
                if pygame.time.get_ticks() - self.daño_timer < 150: #dura 150ms
                    imagen = self.image.copy()
                    imagen.fill((255,0,0), special_flags=pygame.BLEND_RGBA_MULT)   
                else:
                    self.daño_activo = False
                
                #Dibujar siempre usando "imagen"  
            ventana.blit(imagen, self.rect)