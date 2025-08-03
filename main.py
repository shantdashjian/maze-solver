from graphics import Window, Cell


def main():
    win = Window(800, 600)
    cell_1 = Cell(win)
    cell_1.draw(10, 10, 20, 20)

    cell_2 = Cell(win)
    cell_2.draw(100, 100, 200, 150)
    win.wait_for_close()

main()