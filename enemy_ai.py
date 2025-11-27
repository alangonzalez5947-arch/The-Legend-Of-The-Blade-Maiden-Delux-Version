
import pygame
import math

class EnemyAI:
    def __init__(self, speed=2, detection_range=200, flee_range=0):
        self.speed = speed
        self.detection_range = detection_range
        self.flee_range = flee_range

        self.dx = 0
        self.dy = 0
        self.moviendo = False

        self.dir = 1

    def distance(self, x1, y1, x2, y2):
        return math.hypot(x2 - x1, y2 - y1)

    def move_towards(self, enemy, player_pos):
        ex, ey = enemy.rect.center
        px, py = player_pos


        angle = math.atan2(py - ey, px - ex)

        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed



        enemy.rect.x += self.dx
        enemy.rect.y += self.dy


    def move_away(self, enemy, player_pos):
        ex, ey = enemy.rect.center
        px, py = player_pos

        angle = math.atan2(ey - py, ex - px)
        
        self.dx = self.speed * math.cos(angle)
        self.dy = self.speed * math.sin(angle)

        enemy.rect.x += self.dx
        enemy.rect.y += self.dy

    def patrol(self, enemy):
        self.dx = self.speed * self.dir
        self.dy = 0

        enemy.rect.x += self.dx

        if enemy.rect.left < 50 or enemy.rect.right > 750:
            self.dir *= -1

    def update(self, enemy, player_pos):
        dist = self.distance(enemy.rect.centerx, enemy.rect.centery,
                             player_pos[0], player_pos[1])
        

        if dist < self.detection_range:
            self.move_towards(enemy, player_pos)   # persigue al jugador
        else:
            self.patrol(enemy)                     # patrulla

            self.moviendo = (abs(self.dx) > 0.1 or abs(self.dy) > 0.1)

    def attack(self, enemy, player_pos):
        dist = self.distance(enemy.rect.centerx, enemy.rect.centery,    
                             player_pos[0], player_pos[1])  # ataca si está cerca
        
        if dist < self.flee_range:
            self.move_away(enemy, player_pos)   