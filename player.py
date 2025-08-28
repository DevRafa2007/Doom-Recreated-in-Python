import pygame as pg
import math
from settings import *

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = 1.5, 13.5  # Nova posição inicial
        self.angle = PLAYER_ANGLE
        self.rel = 0
        self.shot = False
        self.score = 0  # Sistema de pontuação
        self.kills = 0  # Contador de kills
        self.check_kill = False  # Flag para verificar se matou um NPC

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy)

        # rotação com o mouse
        rel_x, rel_y = pg.mouse.get_rel()
        self.rel = rel_x
        self.angle += rel_x * PLAYER_ROT_SPEED
        
        # Mantém o mouse no centro da tela
        pg.mouse.set_pos(HALF_WIDTH, HALF_HEIGHT)

    def check_wall_collision(self, dx, dy):
        # Adiciona uma pequena margem de colisão
        margin = 0.3
        next_x = self.x + dx
        next_y = self.y + dy

        # Checa colisão com margem
        if not self.game.map.world_map.get((int(next_x + margin * dx), int(self.y))):
            if not self.game.map.world_map.get((int(next_x - margin * dx), int(self.y))):
                self.x = next_x

        if not self.game.map.world_map.get((int(self.x), int(next_y + margin * dy))):
            if not self.game.map.world_map.get((int(self.x), int(next_y - margin * dy))):
                self.y = next_y

    def update(self):
        self.movement()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def get_damage(self, damage):
        self.game.hud.take_damage(damage)