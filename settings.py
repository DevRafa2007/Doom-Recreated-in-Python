import math

# configurações da janela
RES = WIDTH, HEIGHT = 1200, 800
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60

# configurações do jogador
PLAYER_POS = 1.5, 5  # posição inicial x, y
PLAYER_ANGLE = 0  # ângulo inicial
PLAYER_SPEED = 0.005
PLAYER_ROT_SPEED = 0.002

# configurações do raycasting
FOV = math.pi / 2.2  # ~82 graus em radianos para visibilidade ainda melhor
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH  # Dobrado o número de raios para melhor qualidade
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 40  # Aumentado ainda mais para melhor visualização à distância

# configurações de escala
SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)  #dividindo
SCALE = WIDTH // NUM_RAYS

# Tamanho de textura
TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2

# Cores
FLOOR_COLOR = (30, 30, 30)