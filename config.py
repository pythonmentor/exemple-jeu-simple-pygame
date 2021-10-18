"""Initialisation et définition des toutes les constantes du jeu."""
# Directions
RIGHT = (1, 0)
LEFT = (-1, 0)

# Constantes liées au fonctionnement interne du jeu
WIDTH = 10
HEIGHT = 15
BLOCK_START = WIDTH // 2, -1

# Constantes liées à l'interface
UI_TITLE = "DocGame"
UI_BLOCK_SIZE = 50
UI_SCREEN_SIZE = (WIDTH * UI_BLOCK_SIZE, HEIGHT * UI_BLOCK_SIZE)
UI_BLOCK_CURRENT_COLOR = 'Gold'
UI_BLOCK_OLD_COLOR = 'Red'
UI_BACKGROUND_COLOR = (10, 10, 10)
UI_TIMER = 1000
UI_TIMER_ACCELERATION = 0.95
UI_TIMER_MIN = 25
UI_FRAME_RATE = 40  # frames per second
UI_KEY_REPEAT_DELAY = 150
