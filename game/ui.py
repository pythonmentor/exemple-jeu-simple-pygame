"""Ce module contrôle la logique liée à l'interface utilisateur du jeu."""

import pygame

import config
from . import engine

pygame.init()

BLOCK_DOWN_EVENT = pygame.USEREVENT + 0


def create_app():
    """Crée une nouvelle application."""

    # Initialisations pygame
    pygame.display.set_caption(config.UI_TITLE)
    pygame.time.set_timer(BLOCK_DOWN_EVENT, config.UI_TIMER, True)
    pygame.key.set_repeat(config.UI_KEY_REPEAT_DELAY)

    return {
        'screen': pygame.display.set_mode(config.UI_SCREEN_SIZE),
        'timer': config.UI_TIMER,
        'board': engine.create_board(),
        'clock': pygame.time.Clock(),
    }


def run(app):
    """Démarre l'interface graphique du jeu et gère la boucle événementielle."""
    app['running'] = True
    while app['running']:
        _handle_events(app)
        _refresh_screen(app)
    pygame.quit()


def stop(app):
    """Arrête l'application."""
    app['running'] = False


def _handle_events(app):
    """Gère les événements reçu par l'application."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop(app)

        elif event.type == BLOCK_DOWN_EVENT:
            pygame.time.set_timer(BLOCK_DOWN_EVENT, app['timer'], True)
            engine.move_down(app['board'])

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                engine.move_left(app['board'])
            elif event.key == pygame.K_RIGHT:
                engine.move_right(app['board'])
            elif event.key == pygame.K_DOWN:
                engine.move_down(app['board'])


def _draw_block(block, color):
    """Dessine un block sur l'écran."""
    x, y = block
    screen = pygame.display.get_surface()
    pygame.draw.rect(
        screen,
        color,
        (
            x * config.UI_BLOCK_SIZE,
            y * config.UI_BLOCK_SIZE,
            config.UI_BLOCK_SIZE,
            config.UI_BLOCK_SIZE,
        ),
    )


def _refresh_screen(app):
    """Mets à jour l'interface utilisation en fonction des mises à jour du back-end"""
    # On met à jour le back-end
    current, blocks, block_created, game_over = engine.update(app['board'])

    # On dessine le fond de l'écran
    app['screen'].fill(config.UI_BACKGROUND_COLOR)

    # On dessine le block manipulé par l'utilisateur
    _draw_block(current, config.UI_BLOCK_CURRENT_COLOR)

    # On dessine les anciens blocs encore visibles
    for block in blocks:
        _draw_block(block, config.UI_BLOCK_OLD_COLOR)

    # Lorsqu'un nouveau bloc est créé, on accélère le jeu
    if block_created:
        timer = app['timer'] * config.UI_TIMER_ACCELERATION
        app['timer'] = max(int(timer), config.UI_TIMER_MIN)

    # Lorsqu'un bloc atteint le sommet du plateau, on abdique
    if game_over:
        stop(app)

    # On rafraîchit l'écran et contrôle la vitesse de la boucle de jeu
    pygame.display.update()
    app['clock'].tick(config.UI_FRAME_RATE)
