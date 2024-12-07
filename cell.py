import pygame


class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value  # The actual value in the cell (0 for empty)
        self.sketch = 0  # Sketched value (temporary input, 0 if no sketch)
        self.row = row  # Row position of the cell
        self.col = col  # Column position of the cell
        self.screen = screen  # PyGame screen object for rendering
        self.x = col * 60  # X position of the cell (cell width = 60px)
        self.y = row * 60  # Y position of the cell (cell height = 60px)
        self.selected = False  # Flag to track if the cell is selected

    def set_cell_value(self, value):
        """Set the actual value of the cell."""
        self.value = value

    def set_sketched_value(self, value):
        """Set the sketched (temporary) value of the cell."""
        self.sketch = value

    def draw(self):
        """Draw the cell, including the value or sketched value."""
        font = pygame.font.SysFont("arial", 32)

        # Draw the background (either white or red outline if selected)
        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x, self.y, 60, 60), 3)
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y, 60, 60))

        # Draw the value (if it is non-zero, draw it inside the cell)
        if self.value != 0:
            value_text = font.render(str(self.value), True, (0, 0, 0))
            self.screen.blit(value_text, (self.x + 20, self.y + 15))
        # Draw the sketched value in the top-left corner
        elif self.sketch != 0:
            sketch_text = font.render(str(self.sketch), True, (192, 192, 192))
            self.screen.blit(sketch_text, (self.x + 5, self.y + 5))
