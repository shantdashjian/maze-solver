from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("Maze Solver")
        self.canvas = Canvas(self.root, bg="white", height=height, width=width)
        self.canvas.pack(fill=BOTH, expand=1)
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)
    
    def redraw(self):
        self.root.update_idletasks()
        self.root.update()
    
    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
        print("Window closed...")
    
    def close(self):
        self.running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def draw(self, canvas, fill_color="black"):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )

class Cell:
    def __init__(self, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.x1 = -1
        self.y1 = -1
        self.x2 = -1
        self.y2 = -1
        self.win = win
    
    def draw(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        top_left_corner = Point(self.x1, self.y1)
        top_right_corner = Point(self.x2, self.y1)
        bottom_right_corner = Point(self.x2, self.y2)
        bottom_left_corner = Point(self.x1, self.y2)
        if self.has_top_wall:
            self.win.draw_line(Line(top_left_corner, top_right_corner))
        if self.has_right_wall:
            self.win.draw_line(Line(top_right_corner, bottom_right_corner))
        if self.has_bottom_wall:
            self.win.draw_line(Line(bottom_right_corner, bottom_left_corner))
        if self.has_left_wall:
            self.win.draw_line(Line(bottom_left_corner, top_left_corner))