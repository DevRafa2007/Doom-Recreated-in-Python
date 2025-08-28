import pygame as pg
import os
from collections import defaultdict, deque
from settings import *
import math

class SpriteObject:
    def __init__(self, game, path='resources/sprites/npc/caco_demon/0.png', 
                 pos=(10.5, 5.5), scale=0.7, shift=0.27):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

    def get_sprite_projection(self):
        # Calcula o tamanho do sprite baseado na distância
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        # Redimensiona a imagem
        image = pg.transform.scale(self.image, (proj_width, proj_height))

        # Calcula a posição na tela
        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = (self.screen_x - self.sprite_half_width, 
               HALF_HEIGHT - proj_height // 2 + height_shift)

        # Aplica escurecimento baseado na distância
        darkness = max(0.3, min(1.0, 1.0 - (self.norm_dist * 0.02)))
        dark_surface = pg.Surface(image.get_size()).convert_alpha()
        dark_surface.fill((int(darkness * 255),) * 3)
        image.blit(dark_surface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)

        return self.norm_dist, image, pos

    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        while delta < -math.pi:
            delta += 2 * math.pi
        while delta > math.pi:
            delta -= 2 * math.pi

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if self.norm_dist > 0.5:
            return self.get_sprite_projection()
        return False

    def update(self):
        return self.get_sprite()


class AnimatedSprite(SpriteObject):
    def __init__(self, game, path, pos=(10.5, 5.5), scale=0.8, shift=0.15, animation_time=120):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        self.check_animation_time()
        self.animate(self.images)
        return super().update()

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)) and file_name.endswith('.png'):
                img = pg.image.load(os.path.join(path, file_name)).convert_alpha()
                images.append(img)
        return images
