from tkinter import Tk, BOTH, Canvas
import time, random

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
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
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
        if not self.win:
            return
        if self.has_top_wall:
            self.win.draw_line(Line(top_left_corner, top_right_corner))
        else:
            self.win.draw_line(Line(top_left_corner, top_right_corner), "white")
        if self.has_right_wall:
            self.win.draw_line(Line(top_right_corner, bottom_right_corner))
        else:
            self.win.draw_line(Line(top_right_corner, bottom_right_corner), "white")
        if self.has_bottom_wall:
            self.win.draw_line(Line(bottom_right_corner, bottom_left_corner))
        else:
            self.win.draw_line(Line(bottom_right_corner, bottom_left_corner), "white")
        if self.has_left_wall:
            self.win.draw_line(Line(bottom_left_corner, top_left_corner))
        else:
            self.win.draw_line(Line(bottom_left_corner, top_left_corner), "white")

    def draw_move(self, to_cell, undo=False):
        if not undo:
            color = "red"
        else:
            color = "gray"
        self_center = Point((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)
        other_center = Point((to_cell.x1 + to_cell.x2) // 2, (to_cell.y1 + to_cell.y2) // 2)
        if not self.win:
            return
        self.win.draw_line(Line(self_center, other_center), color)

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows 
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.cells = []
        if seed:
            random.seed(seed)
        self.create_cells()
        self.break_entrance_and_exit()
        self.break_walls_r(0, 0)
        self.reset_cells_visited()
    
    def create_cells(self):
        for c in range(self.num_cols):
            self.cells.append([])
            for r in range(self.num_rows):
                self.cells[c].append(Cell(self.win))

        for c in range(self.num_cols):
            for r in range(self.num_rows):
                self.draw_cell(c, r)
    
    def draw_cell(self, i, j):
        x1 = self.x1 + (i * self.cell_size_x)
        y1 = self.y1 + (j * self.cell_size_y)
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self.cells[i][j].draw(x1, y1, x2, y2)
        self.animate()
    
    def animate(self):
        if not self.win:
            return
        self.win.redraw()
        time.sleep(0.01)
    
    def break_entrance_and_exit(self):
        self.cells[0][0].has_top_wall = False
        self.draw_cell(0, 0)
        self.cells[-1][-1].has_bottom_wall = False
        self.draw_cell(self.num_cols - 1, self.num_rows - 1)
    
    def break_walls_r(self, i, j):
        self.cells[i][j].visited = True
        directions = [
            [1, 0], [0, 1], [-1, 0], [0, -1]
        ]
        while True:
            to_visit = []
            for direction in directions:
                column = i + direction[0]
                row = j + direction[1]
                if column < 0 or column >= self.num_cols or row < 0 or row >= self.num_rows:
                    continue
                if self.cells[column][row].visited == False:
                    to_visit.append(direction)
            if not to_visit:
                self.draw_cell(i, j)
                return
            else:
                direction = random.randint(0, len(to_visit) - 1)
                neighbor_i = i + to_visit[direction][0]
                neighbor_j = j + to_visit[direction][1]
                if to_visit[direction] == directions[0]:
                    self.cells[i][j].has_right_wall = False
                    self.cells[neighbor_i][neighbor_j].has_left_wall = False
                elif to_visit[direction] == directions[1]:
                    self.cells[i][j].has_bottom_wall = False
                    self.cells[neighbor_i][neighbor_j].has_top_wall = False
                elif to_visit[direction] == directions[2]:
                    self.cells[i][j].has_left_wall = False
                    self.cells[neighbor_i][neighbor_j].has_right_wall = False
                elif to_visit[direction] == directions[3]:
                    self.cells[i][j].has_top_wall = False
                    self.cells[neighbor_i][neighbor_j].has_bottom_wall = False
                self.break_walls_r(neighbor_i, neighbor_j)
            
    def reset_cells_visited(self):
        for c in range(self.num_cols):
            for r in range(self.num_rows):
                self.cells[c][r].visited = False
    
    def solve(self):
        return self.solve_r(0, 0)
    
    def solve_r(self, i, j):
        self.animate()
        cell = self.cells[i][j]
        cell.visited = True
        if (
            i == self.num_cols - 1 and j == self.num_rows - 1
        ):
            return True
        directions = [
            [1, 0], [0, 1], [-1, 0], [0, -1]
        ]
        for direction in directions:
            column = i + direction[0]
            row = j + direction[1]
            if column < 0 or column >= self.num_cols or row < 0 or row >= self.num_rows:
                continue
            next = self.cells[column][row]
            if self.no_wall(cell, direction) and self.cells[column][row].visited == False:
                cell.draw_move(next)
                result = self.solve_r(column, row)
                if result:
                    return True
                else:
                    cell.draw_move(next, True)
        return False
    
    def no_wall(self, cell, direction):
        if direction == [1, 0]:
            return not cell.has_right_wall
        elif direction == [0, 1]:
            return not cell.has_bottom_wall
        elif direction == [-1, 0]:
            return not cell.has_left_wall
        elif direction == [0, -1]:
            return not cell.has_top_wall

