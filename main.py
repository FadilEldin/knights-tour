# -------------------------------------------------------------------------------------
# Fadil Eldin
# July 12 2025
# a Python program that visualizes the Knight's Tour problem using PyGame.
# The Knight's Tour is a sequence of moves by a knight on a chessboard such
# that the knight visits every square exactly once.
# Graph Theory Explanation:
# 1. The chessboard can be represented as a graph where each square is a vertex.
# 2. Edges connect squares that are a knight's move apart.
# 3. The Knight's Tour is a Hamiltonian path (visits each vertex exactly once).
# 4. The knight alternates between black and white squares with each move:
#    - From white to black, or black to white (graph is bipartite).
# 5. The solution uses Warnsdorff's algorithm, which prioritizes moves with fewest onward options.
# -------------------------------------------------------------------------------------

import pygame
import sys
import time
from collections import deque

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 640
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (255, 255, 255) #(240, 217, 181)
DARK_SQUARE = (0, 0, 0) #(181, 136, 99)
KNIGHT_COLOR = (50, 50, 200)
MOVE_COLOR = (200, 50, 50, 128)
PATH_COLOR = (50, 200, 50, 128)
FONT_COLOR = (0, 0, 0)
FONT_SIZE = 20

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Knight's Tour")
font = pygame.font.SysFont('Arial', FONT_SIZE)

# Knight's possible moves (dx, dy)
MOVES = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]


def is_valid(x, y, board):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == -1


def draw_board(knight_pos, path, move_number):
    screen.fill(WHITE)

    # Draw chessboard
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Draw path
    for i in range(1, len(path)):
        prev_x, prev_y = path[i - 1]
        curr_x, curr_y = path[i]
        pygame.draw.line(screen, PATH_COLOR,
                         ((prev_y + 0.5) * SQUARE_SIZE, (prev_x + 0.5) * SQUARE_SIZE),
                         ((curr_y + 0.5) * SQUARE_SIZE, (curr_x + 0.5) * SQUARE_SIZE), 3)

    # Draw move numbers
    for i, (x, y) in enumerate(path):
        text = font.render(str(i + 1), True, FONT_COLOR)
        text_rect = text.get_rect(center=((y + 0.5) * SQUARE_SIZE, (x + 0.5) * SQUARE_SIZE))
        screen.blit(text, text_rect)

    # Draw knight
    if knight_pos:
        kx, ky = knight_pos
        pygame.draw.circle(screen, KNIGHT_COLOR, ((ky + 0.5) * SQUARE_SIZE, (kx + 0.5) * SQUARE_SIZE), SQUARE_SIZE // 3)

    pygame.display.flip()


def knights_tour(start_x, start_y):
    # Initialize board
    board = [[-1 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    board[start_x][start_y] = 0
    path = [(start_x, start_y)]

    # Use Warnsdorff's algorithm for heuristic
    for step in range(1, BOARD_SIZE * BOARD_SIZE):
        x, y = path[-1]
        min_degree = BOARD_SIZE + 1
        next_move = None

        # Try all possible moves
        for dx, dy in MOVES:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, board):
                # Count the number of available moves from the next position
                degree = 0
                for ndx, ndy in MOVES:
                    nnx, nny = nx + ndx, ny + ndy
                    if is_valid(nnx, nny, board):
                        degree += 1

                # Update if this move has minimum degree
                if degree < min_degree:
                    min_degree = degree
                    next_move = (nx, ny)

        if next_move is None:
            return False, path  # No solution found

        nx, ny = next_move
        board[nx][ny] = step
        path.append((nx, ny))

        # Draw the current state
        draw_board((nx, ny), path, step)
        pygame.time.delay(500)  # Delay to visualize the process
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    return True, path


def main():
    # Start from (0, 0) - can be changed to any valid position
    start_x, start_y = 0, 0

    # Find the solution
    success, path = knights_tour(start_x, start_y)

    if success:
        print("Knight's Tour Solution:")
        for i, (x, y) in enumerate(path):
            print(f"Step {i + 1}: ({x}, {y}) - {'White' if (x + y) % 2 == 0 else 'Black'} square")

        # Graph theory explanation
        print("\nGraph Theory Explanation:")
        print("1. The chessboard can be represented as a graph where each square is a vertex.")
        print("2. Edges connect squares that are a knight's move apart.")
        print("3. The Knight's Tour is a Hamiltonian path (visits each vertex exactly once).")
        print("4. The knight alternates between black and white squares with each move:")
        print("   - From white to black, or black to white (graph is bipartite).")
        print("5. The solution uses Warnsdorff's algorithm, which prioritizes moves with fewest onward options.")

        # Keep the window open
        while True:
            draw_board(None, path, len(path))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    else:
        print("No solution found for the given starting position.")


if __name__ == "__main__":
    main()