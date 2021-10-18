import config

ALL = {(x, y) for x in range(config.WIDTH) for y in range(config.HEIGHT)}
LAST = {(x, config.HEIGHT - 1) for x in range(config.WIDTH)}
FIRST = {(x, 0) for x in range(config.WIDTH)}

RIGHT = 1, 0
LEFT = -1, 0
DOWN = 0, 1


def _move(block, direction):
    x, y = block
    dx, dy = direction
    return x + dx, y + dy


def _above(blocks):
    return {(x, y - 1) for x, y in blocks}


def create_board():
    """Crée un nouveau plateau de jeu."""
    return {
        'current': config.BLOCK_START,
        'new': config.BLOCK_START,
        'blocks': set(),
    }


def move_left(board):
    """Déplace le bloc courant d'une position vers la gauche."""
    board['new'] = _move(board['new'], LEFT)


def move_right(board):
    """Déplace le bloc courant d'une position vers la droite."""
    board['new'] = _move(board['new'], RIGHT)


def move_down(board):
    """Déplace le bloc courant d'une position vers le bas."""
    board['new'] = _move(board['new'], DOWN)


def update(board):
    """Mets à jour l'état du jeu."""
    created = False

    # Si la dernière ligne est complète, on la supprime et on descend les blocs
    if LAST <= board['blocks']:
        board['blocks'] = board['blocks'] - LAST
        board['blocks'] = {_move(block, DOWN) for block in board['blocks']}

    # Si la nouvelle position est autorisée, on déplace le bloc courant
    if board['new'] in (ALL - board['blocks']):
        board['current'] = board['new']

    # Si le bloc est au sol ou sur un autre bloc, on en crée un nouveau
    if board['current'] in (LAST | _above(board['blocks'])):
        board['blocks'].add(board['current'])
        board['current'], created = config.BLOCK_START, True

    board['new'] = board['current']

    return (
        board['current'],
        board['blocks'],
        created,
        bool(FIRST & board['blocks']),
    )
