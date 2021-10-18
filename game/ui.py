"""Ce module contrôle la logique liée à l'interface utilisateur du jeu."""

import pygame

import config
from .engine import Board

pygame.init()

BLOCK_DOWN_EVENT = pygame.USEREVENT + 0


class Application:
    """Représente l'interface graphique du jeu."""

    def __init__(self):
        """Initialise une nouvelle application."""
        pygame.display.set_caption(config.UI_TITLE)
        pygame.time.set_timer(BLOCK_DOWN_EVENT, config.UI_TIMER, True)
        pygame.key.set_repeat(config.UI_KEY_REPEAT_DELAY)

        self._screen = pygame.display.set_mode(config.UI_SCREEN_SIZE)
        self._timer = config.UI_TIMER
        self._board = Board()
        self._clock = pygame.time.Clock()

        self.running = False

    def run(self):
        """Démarre l'interface graphique du jeu et gère la boucle
        événementielle."""
        self.running = True
        while self.running:
            self._handle_events()
            self._refresh_screen()
        pygame.quit()

    def stop(self):
        """Arrête l'application."""
        self.running = False

    def _handle_events(self):
        """Gère les événements reçu par l'application."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()

            elif event.type == BLOCK_DOWN_EVENT:
                pygame.time.set_timer(BLOCK_DOWN_EVENT, self._timer, True)
                self._board.move('down')

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self._board.move('left')
                elif event.key == pygame.K_RIGHT:
                    self._board.move('right')
                elif event.key == pygame.K_DOWN:
                    self._board.move('down')

    def _draw_block(self, block, color):
        """Dessine un block sur l'écran."""
        x, y = block
        pygame.draw.rect(
            self._screen,
            color,
            (
                x * config.UI_BLOCK_SIZE,
                y * config.UI_BLOCK_SIZE,
                config.UI_BLOCK_SIZE,
                config.UI_BLOCK_SIZE,
            ),
        )

    def _refresh_screen(self):
        """Mets à jour l'interface utilisation en fonction des mises à jour du
        back-end."""
        # On met à jour le back-end: la logique du jeu se déroule ici
        block_created, game_over = self._board.update()

        # On dessine le fond de l'écran
        self._screen.fill(config.UI_BACKGROUND_COLOR)

        # On dessine le block manipulé par l'utilisateur
        self._draw_block(self._board.current, config.UI_BLOCK_CURRENT_COLOR)

        # On dessine les anciens blocs encore visibles
        for block in self._board:
            self._draw_block(block, config.UI_BLOCK_OLD_COLOR)

        # Lorsqu'un nouveau bloc est créé, on accélère le jeu
        if block_created:
            timer = self._timer * config.UI_TIMER_ACCELERATION
            self._timer = max(int(timer), config.UI_TIMER_MIN)

        # Lorsqu'un bloc atteint le sommet du plateau, on abdique
        if game_over:
            self.stop()

        # On rafraîchit l'écran et contrôle la vitesse de la boucle de jeu
        pygame.display.update()
        self._clock.tick(config.UI_FRAME_RATE)
