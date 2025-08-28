import pygame as pg
import math
from settings import *

class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []

    def get_objects_to_render(self):
        self.objects_to_render = []
        
        # Adiciona paredes
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values
            wall_column = (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height)
            wall_object = (depth, wall_column, texture, offset)
            self.objects_to_render.append(wall_object)
        
        # Adiciona NPCs
        for npc in self.game.npc_list:
            sprite = npc.get_sprite()
            if sprite:
                sprite_depth, sprite_image, sprite_pos = sprite
                sprite_object = (sprite_depth, {'type': 'npc', 'data': (sprite_image, sprite_pos)})
                self.objects_to_render.append(sprite_object)
        
        # Ordena objetos por profundidade (mais distantes primeiro)
        self.objects_to_render.sort(key=lambda x: x[0], reverse=True)

    def ray_cast(self):
        self.ray_casting_result = []
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # vertical
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            texture_vert = 1  # textura padrão
            for i in range(MAX_DEPTH):
                vert_tile = int(x_vert), int(y_vert)
                if vert_tile in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[vert_tile]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # horizontal
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            texture_hor = 1  # textura padrão
            for i in range(MAX_DEPTH):
                hor_tile = int(x_hor), int(y_hor)
                if hor_tile in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[hor_tile]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # escolhe a distância mais próxima
            if depth_vert < depth_hor:
                depth = depth_vert
                texture = texture_vert
                y_offset = y_vert % 1
                offset = y_offset if cos_a > 0 else (1 - y_offset)
            else:
                depth = depth_hor
                texture = texture_hor
                x_offset = x_hor % 1
                offset = (1 - x_offset) if sin_a > 0 else x_offset

            # remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)
            
            # projeção
            proj_height = min(int(SCREEN_DIST / (depth + 0.0001)), HEIGHT * 2)
            if proj_height < 1:  # Evita altura zero
                proj_height = 1

            # ray casting result
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()