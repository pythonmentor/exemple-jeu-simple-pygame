import config

ALL = {(x, y) for x in range(config.WIDTH) for y in range(config.HEIGHT)}
LAST = {(x, config.HEIGHT - 1) for x in range(config.WIDTH)}
FIRST = {(x, 0) for x in range(config.WIDTH)}


def _above(blocks):
    return {block.up for block in blocks}


class Block(tuple):
    """Représente un bloc."""

    def __new__(cls, x, y):
        """Construit un nouveau block immutable."""
        return super().__new__(cls, (x, y))

    @property
    def down(self):
        """Nouveau bloc situé en dessous."""
        x, y = self
        return self.__class__(x, y + 1)

    @property
    def up(self):
        """Nouveau bloc situé en dessus."""
        x, y = self
        return self.__class__(x, y - 1)

    @property
    def right(self):
        """Nouveau bloc situé sur la droite."""
        x, y = self
        return self.__class__(x + 1, y)

    @property
    def left(self):
        """Nouveau bloc situé sur la gauche."""
        x, y = self
        return self.__class__(x - 1, y)


class Board:
    """Représente le plateau de jeu."""

    def __init__(self):
        """Crée un nouveau plateau de jeu."""
        self.current = Block(*config.BLOCK_START)
        self._new = self.current
        self._blocks = set()

    def __iter__(self):
        """Permet d'itérer directement sur les blocks avec un boucle for."""
        return iter(self._blocks)

    def move(self, direction):
        """Déplace le bloc courant dans la direction indiquée.

        La direction peut être 'right', 'left', 'down'.
        """
        if direction not in ('right', 'left', 'down'):
            raise ValueError("direction must be in 'right', 'left', 'down'")
        self._new = getattr(self._new, direction)

    def update(self):
        """Mets à jour l'état du jeu."""
        created = False

        # Si la dernière ligne est complète, on la supprime et on descend les blocs
        if LAST <= self._blocks:
            self._blocks = self._blocks - LAST
            self._blocks = {block.down for block in self._blocks}

        # Si la nouvelle position est autorisée, on déplace le bloc courant
        if self._new in (ALL - self._blocks):
            self.current = self._new

        # Si le bloc est au sol ou sur un autre bloc, on en crée un nouveau
        if self.current in (LAST | _above(self._blocks)):
            self._blocks.add(self.current)
            self.current, created = Block(*config.BLOCK_START), True

        self._new = self.current

        return created, bool(FIRST & self._blocks)
