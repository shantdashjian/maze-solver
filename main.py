from graphics import Window, Cell, Maze


def main():
    win = Window(800, 600)
    maze = Maze(100, 100, 5, 5, 50, 50, win)

    win.wait_for_close()

main()