from graphics import Window, Cell, Maze


def main():
    win = Window(800, 600)
    maze = Maze(43, 43, 12, 16, 43, 43, win)
    maze.break_entrance_and_exit()
    win.wait_for_close()

main()