import random

class Piece:
    def __init__(self, shape_type):
        # Custom piece shapes (different from traditional Tetris)
        self.shapes = {
            # Original pieces
            'L_Shape': [
                [1, 0, 0],
                [1, 0, 0],
                [1, 1, 0]
            ],
            'J_Shape': [
                [0, 0, 1],
                [0, 0, 1],
                [0, 1, 1]
            ],
            'S_Shape': [
                [0, 1, 1],
                [1, 1, 0],
                [0, 0, 0]
            ],
            'Z_Shape': [
                [1, 1, 0],
                [0, 1, 1],
                [0, 0, 0]
            ],
            'O_Shape': [
                [1, 1],
                [1, 1]
            ],
            'I_Shape': [
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ],
            # Custom pieces
            'Cross': [
                [0, 1, 0],
                [1, 1, 1],
                [0, 1, 0]
            ],
            'Diamond': [
                [0, 1, 0],
                [1, 1, 1],
                [1, 0, 1]
            ],
            'U_Shape': [
                [1, 0, 1],
                [1, 1, 1]
            ],
            'Plus': [
                [0, 1, 0],
                [1, 1, 1],
                [0, 1, 0]
            ],
            'H_Shape': [
                [1, 0, 1],
                [1, 1, 1],
                [1, 0, 1]
            ],
            'Line_3': [
                [1, 1, 1]
            ]
        }
        
        self.shape_type = shape_type
        self.shape = self.shapes[shape_type]
        self.color = self.get_random_color()
        self.x = 0
        self.y = 0
        
    def get_random_color(self):
        colors = [
            (255, 0, 0),    # Red
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (255, 255, 0),  # Yellow
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Cyan
            (255, 128, 0)   # Orange
        ]
        return random.choice(colors)

    def rotate(self):
        # Rotate the piece 90 degrees clockwise
        rows = len(self.shape)
        cols = len(self.shape[0])
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]
        
        for i in range(rows):
            for j in range(cols):
                rotated[j][rows - 1 - i] = self.shape[i][j]
        
        self.shape = rotated

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def move_down(self):
        self.y += 1

    def get_positions(self):
        positions = []
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j]:
                    positions.append((self.x + j, self.y + i))
        return positions
