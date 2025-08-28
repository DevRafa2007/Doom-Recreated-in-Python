import pygame as pg
from settings import *

class HUD:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.health = 1000  # 50x mais vida 
        self.max_health = 1000  # 50x mais vida
        self.health_recovery_delay = 2000  # 2 segundos
        self.last_hit_time = 0
        self.recovery_rate = 100  # pontos de vida por segundo
        self.last_recovery_time = 0
        self.enemies_killed = 0
        self.required_kills = 20  # Atualizado para 20 kills
        self.digits = self.load_digits()
        
    def load_digits(self):
        digits = []
        digit_size = (30, 45)
        for i in range(11):
            digit_img = pg.image.load(f'resources/textures/digits/{i}.png').convert_alpha()
            digit_img = pg.transform.scale(digit_img, digit_size)
            digits.append(digit_img)
        return digits

    def update(self):
        current_time = pg.time.get_ticks()
        # Recupera vida se não tomou dano recentemente
        if current_time - self.last_hit_time > self.health_recovery_delay:
            if current_time - self.last_recovery_time > 1000:  # A cada segundo
                self.health = min(self.max_health, self.health + self.recovery_rate)
                self.last_recovery_time = current_time

    def draw(self):
        # Desenha barra de vida
        health_width = 200
        health_height = 20
        x = 20
        y = 20
        
        # Barra vermelha (fundo)
        pg.draw.rect(self.screen, (200, 0, 0), (x, y, health_width, health_height))
        # Barra verde (vida atual)
        current_health_width = (self.health / self.max_health) * health_width
        pg.draw.rect(self.screen, (0, 200, 0), (x, y, current_health_width, health_height))
        
        # Desenha número de inimigos mortos com formato "X/20"
        font = pg.font.Font(None, 36)
        kills_text = f"Kills: {self.game.player.kills}/{self.required_kills}"
        kills_surface = font.render(kills_text, True, (200, 200, 200))
        self.screen.blit(kills_surface, (x, y + 30))
        
        # Atualiza o contador de kills
        if self.game.player.check_kill:
            self.enemies_killed = self.game.player.kills  # Sincroniza com as kills do player
            self.game.player.check_kill = False  # Reseta a flag
        
        # Mantém sempre sincronizado com o player
        self.enemies_killed = self.game.player.kills
        
        # Desenha kills
        kills_text = f"Kills: {self.enemies_killed}"
        kills_surface = font.render(kills_text, True, (255, 255, 255))
        self.screen.blit(kills_surface, (WIDTH - 150, 20))
        
        # Desenha score
        score_text = f"Score: {self.game.player.score}"
        score_surface = font.render(score_text, True, (255, 255, 255))
        self.screen.blit(score_surface, (WIDTH - 150, 60))

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)
        self.last_hit_time = pg.time.get_ticks()
        return self.health <= 0

    def add_kill(self):
        self.enemies_killed += 1
        return self.enemies_killed >= self.required_kills
