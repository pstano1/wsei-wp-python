import json
import copy
import random

class Cell:
    def __init__(self, x: int, y: int, initialState: bool) -> None:
        self.x: int = x
        self.y: int = y
        self.alive: bool = initialState

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "alive": self.alive
        } 


class Grid:
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.cells: [[Cell]] = [[Cell(x, y, random.random() > 0.85) for y in range(height)] for x in range(width)]

    def count_alive_neighbors(self, x: int, y: int) -> int:
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        count = 0
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.width and 0 <= new_y < self.height and self.cells[new_x][new_y].alive:
                count += 1
        return count

    def next_generation(self) -> None:
        new_state = copy.deepcopy(self.cells)
        for x in range(self.width):
            for y in range(self.height):
                neighbours_count: int = self.count_alive_neighbors(x, y)

                if self.cells[x][y].alive:
                    if neighbours_count < 2 or neighbours_count > 3:
                        new_state[x][y].alive = False
                    else:
                        new_state[x][y].alive = True
                else:
                    if neighbours_count == 3:
                        new_state[x][y].alive = True

        self.cells = new_state      

    def create_snapshot(self):
        json_grid = [[cell.to_dict() for cell in row] for row in self.cells]
        return json.dumps(json_grid)
    
    def load_from_snapshot(self, json_data) -> None:
        data = json.loads(json_data)

        new_cells = []
        for row in data:
            cell_row = []
            for cell_data in row:
                cell = Cell(cell_data['x'], cell_data['y'], cell_data['alive'])
                cell_row.append(cell)
            new_cells.append(cell_row)

        self.cells = new_cells

