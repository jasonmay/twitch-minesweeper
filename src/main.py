import curses
from interface import Interface




def main(screen):
    size = (25, 16)  # v, h
    interface = Interface(screen, size[0], size[1])
    interface.run()


if __name__ == "__main__":
    curses.wrapper(main)
