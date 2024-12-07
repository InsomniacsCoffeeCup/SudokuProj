import pygame
from cell import Cell
from sudoku_generator import SudokuGenerator  # Importing SudokuGenerator

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty  # Difficulty parameter

        # Create the 9x9 grid of Cell objects
        self.grid = [[Cell(0, row, col, screen) for col in range(9)] for row in range(9)]

        # Initially, no cell is selected
        self.selected_cell = None

        # Initialize the Sudoku generator
        self.sudoku_generator = SudokuGenerator(9, 81 - difficulty)  # Difficulty affects number of cells to be removed
        self.sudoku_generator.fill_values()  # Fill board with values
        self.sudoku_board = self.sudoku_generator.get_board()  # Get the generated board

        # Update the grid with the generated values
        for row in range(9):
            for col in range(9):
                self.grid[row][col].set_cell_value(self.sudoku_board[row][col])

    def draw(self):
        """Draws the board with bold lines for 3x3 boxes and regular grid lines."""
        # Draw grid lines
        for i in range(10):
            line_width = 2 if i % 3 != 0 else 4  # Bold lines for 3x3 subgrids
            pygame.draw.line(self.screen, (0, 0, 0), (i * 60, 0), (i * 60, 540), line_width)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * 60), (540, i * 60), line_width)

        # Draw each cell
        for row in self.grid:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        """Mark a cell as selected."""
        if self.selected_cell:
            self.selected_cell.selected = False
        self.selected_cell = self.grid[row][col]
        self.selected_cell.selected = True

    def click(self, x, y):
        """Return the row, col of the clicked cell, or None if clicked outside."""
        col = x // 60
        row = y // 60
        if row < 9 and col < 9:
            return row, col
        return None

    def clear(self):
        """Clear the value of the selected cell, if the value was user-input."""
        if self.selected_cell and self.selected_cell.value == 0:
            self.selected_cell.set_sketched_value(0)

    def sketch(self, value):
        """Sketch a temporary number in the selected cell."""
        if self.selected_cell and self.selected_cell.value == 0:
            self.selected_cell.set_sketched_value(value)

    def place_number(self, value):
        """Place a number in the selected cell."""
        if self.selected_cell and self.selected_cell.value == 0:
            self.selected_cell.set_cell_value(value)
            self.selected_cell.set_sketched_value(0)  # Clear sketched value after placement

    def reset_to_original(self):
        """Reset all cells to their original value."""
        for row in self.grid:
            for cell in row:
                cell.set_cell_value(0)  # Reset value to 0
                cell.set_sketched_value(0)  # Clear sketched value

    def is_full(self):
        """Check if the board is fully filled (no zeros left)."""
        for row in self.grid:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def update_board(self):
        """Update the underlying 2D board with the values from the cells."""
        updated_board = []
        for row in self.grid:
            updated_row = [cell.value for cell in row]
            updated_board.append(updated_row)
        return updated_board

    def find_empty(self):
        """Find the first empty cell (value == 0) and return its (row, col)."""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j].value == 0:
                    return i, j
        return None

    def check_board(self):
        """Check if the Sudoku board is correctly solved (all rules are satisfied)."""
        for i in range(9):
            row_values = [self.grid[i][j].value for j in range(9)]
            col_values = [self.grid[j][i].value for j in range(9)]
            if len(set(row_values)) != 9 or len(set(col_values)) != 9:
                return False

        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box_values = []
                for i in range(3):
                    for j in range(3):
                        box_values.append(self.grid[box_row + i][box_col + j].value)
                if len(set(box_values)) != 9:
                    return False

        return True
