import pygame as pg
from settings import *

class Weapon:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.images = self.load_images()
        self.frame_counter = 0
        self.frame_rate = 10
        self.state = 'idle'
        self.current_frame = 0
        self.shooting = False
        self.reloading = False
        self.ammo = 6
        self.shot_length = 2
        self.reload_length = 5
        self.shot_cooldown = 500  # tempo em milissegundos entre tiros
        self.last_shot_time = 0
        self.digits = self.load_digits()
        self.damage = 50
        
        try:
            self.shoot_sound = pg.mixer.Sound('resources/sound/shotgun.wav')
            self.shoot_sound.set_volume(0.4)
        except:
            print("Erro ao carregar som da arma")

    def load_images(self):
        weapon_size = (WIDTH // 3, HEIGHT // 2)
        images = []
        for i in range(6):
            path = f'resources/sprites/weapon/shotgun/{i}.png'
            weapon_img = pg.image.load(path).convert_alpha()
            weapon_img = pg.transform.scale(weapon_img, weapon_size)
            images.append(weapon_img)
        return images

    def load_digits(self):
        digits = []
        digit_size = (30, 45)
        for i in range(11):  # 0-10
            digit_img = pg.image.load(f'resources/textures/digits/{i}.png').convert_alpha()
            digit_img = pg.transform.scale(digit_img, digit_size)
            digits.append(digit_img)
        return digits

    def update(self):
        self.check_animation_time()
        self.input()

    def input(self):
        keys = pg.key.get_pressed()
        mouse = pg.mouse.get_pressed()
        
        current_time = pg.time.get_ticks()
        if (mouse[0] and not self.shooting and not self.reloading and 
            current_time - self.last_shot_time > self.shot_cooldown):
            self.shoot()
        
        if keys[pg.K_r] and not self.reloading and self.ammo < 6:
            self.reload()

    def shoot(self):
        if self.ammo > 0 and not self.shooting and not self.reloading:
            self.shooting = True
            self.state = 'shoot'
            self.current_frame = 1
            self.ammo -= 1
            self.shoot_sound.play()
            self.last_shot_time = pg.time.get_ticks()

            hit_npcs = []
            for npc in self.game.npc_list:
                if npc.alive and npc.ray_cast_player_npc():
                    if HALF_WIDTH - npc.sprite_half_width < npc.screen_x < HALF_WIDTH + npc.sprite_half_width:
                        hit_npcs.append(npc)
            
            if hit_npcs:
                closest_npc = min(hit_npcs, key=lambda npc: npc.dist)
                closest_npc.take_damage(self.damage)

    def reload(self):
        if not self.reloading and not self.shooting and self.ammo < 6:
            self.reloading = True
            self.state = 'reload'
            self.current_frame = 3

    def draw(self):
        # Desenha a arma
        weapon_pos = self.get_weapon_position()
        current_image = self.images[self.current_frame]
        self.screen.blit(current_image, weapon_pos)
        
        # Desenha o contador de munição
        x = WIDTH - 100
        y = HEIGHT - 100
        ammo_img = self.digits[min(self.ammo, 10)]
        self.screen.blit(ammo_img, (x, y))

    def get_weapon_position(self):
        weapon_x = WIDTH // 2 - self.images[0].get_width() // 2
        weapon_y = HEIGHT - self.images[0].get_height() + 100
        return weapon_x, weapon_y

    def check_animation_time(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_counter = 0
            
            if self.shooting:
                if self.current_frame < self.shot_length:
                    self.current_frame += 1
                else:
                    self.shooting = False
                    self.state = 'idle'
                    self.current_frame = 0
            
            elif self.reloading:
                if self.current_frame < self.reload_length:
                    self.current_frame += 1
                    if self.current_frame == self.reload_length:
                        self.ammo = 6
                else:
                    self.reloading = False
                    self.state = 'idle'
                    self.current_frame = 0
