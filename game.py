import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from weapon import *
from sprite_object import *
from npc import *
from random import choices, randrange
from hud import HUD
from pathfinding import PathFinding
from sound import Sound

class Game:
    def __init__(self):
        pg.init()
        print("Initializing game and setting mouse to invisible")
        pg.mouse.set_visible(False)  # O cursor começa invisível
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.sound = Sound(self)
        self.game_state = 'playing'  # estados: 'playing', 'game_over', 'win'
        self.wave = 1
        self.new_game()

    def new_game(self):
        # Reset game state
        self.game_state = 'playing'
        pg.mouse.set_visible(False)
        self.wave = 1
        
        # Inicializa componentes do jogo
        self.map = Map()
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.weapon = Weapon(self)
        self.hud = HUD(self)
        self.pathfinding = PathFinding(self)
        
        # Configura os tipos de NPCs
        self.npc_types = {
            'soldier': {'path': 'resources/sprites/npc/soldier/0.png', 'scale': 0.6, 'shift': 0.38},
            'caco_demon': {'path': 'resources/sprites/npc/caco_demon/0.png', 'scale': 0.7, 'shift': 0.27},
            'cyber_demon': {'path': 'resources/sprites/npc/cyber_demon/0.png', 'scale': 1.0, 'shift': 0.04}
        }
        
        # Reset NPCs
        self.npc_list = []
        self.npc_positions = self.get_npc_positions()
        self.spawn_npc()
        
        # Reset player stats
        self.player.kills = 0
        self.hud.health = self.hud.max_health

    def check_game_state(self):
        # Verifica condição de vitória (20 kills)
        if self.player.kills >= 20 and self.game_state == 'playing':
            self.game_state = 'win'
            pg.mouse.set_visible(True)
        
        # Verifica condição de derrota (vida = 0)
        if self.hud.health <= 0 and self.game_state == 'playing':
            self.game_state = 'game_over'
            pg.mouse.set_visible(True)
    
    def draw_button(self, text, position):
        button_width = 200
        button_height = 50
        button_x = position[0] - button_width // 2
        button_y = position[1] - button_height // 2
        
        # Desenha o botão
        button_rect = pg.Rect(button_x, button_y, button_width, button_height)
        mouse_pos = pg.mouse.get_pos()
        
        # Muda a cor se o mouse estiver sobre o botão
        if button_rect.collidepoint(mouse_pos):
            pg.draw.rect(self.screen, (150, 0, 0), button_rect)
        else:
            pg.draw.rect(self.screen, (100, 0, 0), button_rect)
            
        # Desenha o texto do botão
        font = pg.font.Font(None, 36)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=position)
        self.screen.blit(text_surface, text_rect)
        
        return button_rect

    def draw_end_screen(self):
        if self.game_state in ['win', 'game_over']:
            # Carrega e desenha a imagem apropriada
            image_path = 'resources/textures/win.png' if self.game_state == 'win' else 'resources/textures/game_over.png'
            try:
                screen_image = pg.image.load(image_path).convert_alpha()
                screen_image = pg.transform.scale(screen_image, (WIDTH, HEIGHT))
                self.screen.blit(screen_image, (0, 0))
            except:
                # Fallback se a imagem não carregar
                self.screen.fill((0, 0, 0))
                font = pg.font.Font(None, 74)
                text = "YOU WIN!" if self.game_state == 'win' else "GAME OVER"
                text_surface = font.render(text, True, (255, 0, 0))
                text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//3))
                self.screen.blit(text_surface, text_rect)
            
            # Desenha o botão de reinício
            button_rect = self.draw_button("Restart Game", (WIDTH//2, HEIGHT*3//4))
            
            # Verifica clique no botão
            if pg.mouse.get_pressed()[0]:  # Botão esquerdo do mouse
                mouse_pos = pg.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    self.game_state = 'playing'
                    pg.mouse.set_visible(False)
                    self.new_game()
    
    def update(self):
        if self.game_state == 'playing':
            self.player.update()
            self.raycasting.update()
            self.object_renderer.update()
            self.weapon.update()
            self.hud.update()
            
            # Atualiza todos os NPCs
            for npc in self.npc_list:
                npc.update()

            if not self.npc_list and self.wave == 1:
                self.wave = 2
                self.spawn_npc()
            
            # Verifica condições de vitória/derrota
            self.check_game_state()
        
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        self.player.shot = False  # Reseta o tiro para o próximo frame

    def draw(self):
        self.screen.fill('black')
        
        if self.game_state == 'playing':
            self.object_renderer.draw()
            self.weapon.draw()
            self.hud.draw()
        else:
            self.draw_end_screen()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True

    def get_npc_positions(self):
        positions = []
        for i in range(len(self.map.map)):
            for j in range(len(self.map.map[0])):
                if self.map.map[i][j] == 0:  # Espaço vazio
                    positions.append((j + 0.5, i + 0.5))
        return positions

    def spawn_npc(self):
        # Spawn de 20 NPCs
        num_npcs = 20
        
        # Probabilidades de spawn para cada tipo de NPC
        weights = [0.7, 0.2, 0.1]  # 70% soldier, 20% caco_demon, 10% cyber_demon
        npc_types_list = ['soldier', 'caco_demon', 'cyber_demon']
        
        # Escolhe posições aleatórias para os NPCs
        available_positions = self.npc_positions.copy()
        
        for _ in range(num_npcs):
            if not available_positions:
                break
                
            pos = available_positions.pop(randrange(len(available_positions)))
            npc_type = choices(npc_types_list, weights)[0]
            npc_params = self.npc_types[npc_type]
            
            self.npc_list.append(
                NPC(self, 
                    path=npc_params['path'],
                    pos=pos,
                    scale=npc_params['scale'],
                    shift=npc_params['shift'])
            )

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
