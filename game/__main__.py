"""Lancement du jeu."""

from .ui import Application


def main():
    """Point d'entrée principal du jeu."""
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
