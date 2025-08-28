import pygame as pg
import os

class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound/'
        self.sounds = {}
        
        try:
            # Carrega os sons dos NPCs
            if os.path.exists(self.path + 'npc_shot.wav'):
                self.npc_shot = pg.mixer.Sound(self.path + 'npc_shot.wav')
                self.npc_shot.set_volume(0.2)
            else:
                print("Arquivo de som não encontrado:", self.path + 'npc_shot.wav')
                self.npc_shot = None
                
            if os.path.exists(self.path + 'npc_pain.wav'):
                self.npc_pain = pg.mixer.Sound(self.path + 'npc_pain.wav')
                self.npc_pain.set_volume(0.2)
            else:
                print("Arquivo de som não encontrado:", self.path + 'npc_pain.wav')
                self.npc_pain = None
                
            if os.path.exists(self.path + 'npc_death.wav'):
                self.npc_death = pg.mixer.Sound(self.path + 'npc_death.wav')
                self.npc_death.set_volume(0.2)
            else:
                print("Arquivo de som não encontrado:", self.path + 'npc_death.wav')
                self.npc_death = None
            
            # Sons do jogador
            if os.path.exists(self.path + 'shotgun.wav'):
                self.player_shot = pg.mixer.Sound(self.path + 'shotgun.wav')
                self.player_shot.set_volume(0.2)
            else:
                print("Arquivo de som não encontrado:", self.path + 'shotgun.wav')
                self.player_shot = None

            if os.path.exists(self.path + 'player_pain.wav'):
                self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav')
                self.player_pain.set_volume(0.2)
            else:
                print("Arquivo de som não encontrado:", self.path + 'player_pain.wav')
                self.player_pain = None
            
            # Música tema
            if os.path.exists(self.path + 'theme.mp3'):
                pg.mixer.music.load(self.path + 'theme.mp3')
                pg.mixer.music.set_volume(0.2)
            else:
                print("Arquivo de som não encontrado:", self.path + 'theme.mp3')
        except Exception as e:
            print("Erro ao carregar sons:", str(e))
