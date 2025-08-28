import pygame as pg
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = pg.image.load('resources/textures/sky.png').convert()
        self.sky_offset = 0

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),
        }

    def update(self):
        self.sky_offset = (self.sky_offset + 1.0 * self.game.player.rel) % WIDTH

    def draw(self):
        self.draw_background()
        self.render_game_objects()

    def draw_background(self):
        # Desenha o céu com movimento parallax
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        
        # Desenha o chão
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def render_wall(self, depth, wall_column, texture, offset):
        wall_pos = (wall_column[0], wall_column[1])
        wall_width = wall_column[2]
        wall_height = wall_column[3]
        wall = self.wall_textures[texture]
        
        # Pega a coluna correta da textura
        texture_x = int(offset * (wall.get_width() - 1))
        wall_piece = wall.subsurface(texture_x, 0, 1, wall.get_height())
        wall_scaled = pg.transform.scale(wall_piece, (wall_width, wall_height))
        
        # Aplica escurecimento baseado na distância
        darkness = max(0.3, min(1.0, 1.0 - (depth * 0.02)))
        dark_surface = pg.Surface(wall_scaled.get_size()).convert_alpha()
        dark_surface.fill((int(darkness * 255),) * 3)
        wall_scaled.blit(dark_surface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        
        # Desenha a parede
        self.screen.blit(wall_scaled, wall_pos)

    def render_npc(self, depth, image, pos):
        # Ajuste da visualização baseado na distância
        darkness = max(0.5, min(1.0, 1.0 - (depth * 0.01)))  # Suaviza o escurecimento
        
        # Aplica escurecimento mais suave
        dark_surface = pg.Surface(image.get_size()).convert_alpha()
        dark_surface.fill((int(darkness * 255),) * 3)
        darkened_image = image.copy()
        darkened_image.blit(dark_surface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        
        # Aplica um leve efeito de transparência baseado na distância
        alpha = max(100, min(255, 255 - int(depth * 3)))
        darkened_image.set_alpha(alpha)
        
        # Desenha o NPC
        self.screen.blit(darkened_image, pos)

    def render_game_objects(self):
        # Ordena os objetos por profundidade (mais distantes primeiro)
        objects = sorted(self.game.raycasting.objects_to_render, key=lambda x: x[0], reverse=True)
        
        for obj in objects:
            if len(obj) == 4:  # É uma parede
                depth, wall_column, texture, offset = obj
                self.render_wall(depth, wall_column, texture, offset)
            elif len(obj) == 2:  # É um NPC/sprite
                depth, sprite_data = obj
                if isinstance(sprite_data, dict) and sprite_data.get('type') == 'npc':
                    image, pos = sprite_data['data']
                    self.render_npc(depth, image, pos)