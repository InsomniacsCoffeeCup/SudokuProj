import pygame

class Cell:
    def __init__(self, row, col, value, board_width, board_height):
        self.row = row
        self.col = col
        self.value = value
        self.sketch = 0
        self.selected = False
        self.cell_width = board_width // 9
        self.cell_height = board_height // 9

    def draw(self, screen):
        font = pygame.font.SysFont("arial", 40)
        if self.value != 0:
            text = font.render(str(self.value), True, (0, 0, 0))
            x = self.col * self.cell_width + 15
            y = self.row * self.cell_height + 15
            screen.blit(text, (x, y))
        elif self.sketch != 0:
            sketch_font = pygame.font.SysFont("arial", 20)
            sketch_text = sketch_font.render(str(self.sketch), True, (128, 128, 128))
            x = self.col * self.cell_width + 5
            y = self.row * self.cell_height + 5
            screen.blit(sketch_text, (x, y))

        if self.selected:
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                (self.col * self.cell_width, self.row * self.cell_height, self.cell_width, self.cell_height),
                3,
            )


class Board:
    def __init__(self, width, height, screen, board_data):
        self.width = width
        self.height = height
        self.screen = screen
        self.board_data = board_data
        self.cells = [[Cell(row, col, self.board_data[row][col], width, height) for col in range(9)] for row in range(9)]
        self.selected_cell = None

    def draw(self):
        cell_size = self.width // 9
        for i in range(10):
            line_thickness = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * cell_size), (self.width, i * cell_size), line_thickness)
            pygame.draw.line(self.screen, (0, 0, 0), (i * cell_size, 0), (i * cell_size, self.height), line_thickness)

        for row in self.cells:
            for cell in row:
                cell.draw(self.screen)

    def select(self, row, col):
        if self.selected_cell:
            self.cells[self.selected_cell[0]][self.selected_cell[1]].selected = False
        self.cells[row][col].selected = True
        self.selected_cell = (row, col)

    def click(self, x, y):
        cell_size = self.width // 9
        if 0 <= x < self.width and 0 <= y < self.height:
            row = y // cell_size
            col = x // cell_size
            return row, col
        return None

    def clear(self):
        if self.selected_cell:
            row, col = self.selected_cell
            cell = self.cells[row][col]
            if cell.value == 0:
                cell.sketch = 0

    def sketch(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            cell = self.cells[row][col]
            if cell.value == 0:
                cell.sketch = value

    def place_number(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            cell = self.cells[row][col]
            if cell.value == 0:
                cell.value = value
                cell.sketch = 0

    def reset_to_original(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    cell.sketch = 0

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def update_board(self):
        for row in self.cells:
            for cell in row:
                self.board_data[cell.row][cell.col] = cell.value

    def find_empty(self):
        for row in range(9):
            for col in range(9):
                if self.board_data[row][col] == 0:
                    return row, col
        return None

    def check_board(self):
        pass
