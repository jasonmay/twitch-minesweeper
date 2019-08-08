import curses
from interface import Interface


def main(screen):
    size = (25, 16)  # v, h
    mines = 10
    interface = Interface(screen, size[0], size[1], mines)
    interface.run()


if __name__ == "__main__":
    curses.wrapper(main)
