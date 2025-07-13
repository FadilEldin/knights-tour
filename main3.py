import pygame
import sys
import time
from collections import deque

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1300, 800
BOARD_SIZE = 8
SQUARE_SIZE = 70
CHESSBOARD_LEFT = (WIDTH - BOARD_SIZE * SQUARE_SIZE) // 2
CHESSBOARD_TOP = 40
GRAPH_TOP = CHESSBOARD_TOP + BOARD_SIZE * SQUARE_SIZE + 40
GRAPH_LEFT = 40
GRAPH_NODE_SPACING = 40  # Fixed typo in variable name
GRAPH_NODE_SIZE = 15
BACKGROUND_COLOR = (240, 217, 181)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURE_WHITE = (255, 255, 255)
PURE_BLACK = (0, 0, 0)
PATH_COLOR = (50, 200, 50)
FONT_COLOR = (0, 0, 0)
BOARD_FONT_SIZE = 20  # Larger font for board squares
GRAPH_FONT_SIZE = 12
GRAPH_LINE_COLOR = (100, 100, 100)
GRAPH_ROW_SPACING = 50

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Knight's Tour - Graph Theory Visualization")
board_font = pygame.font.SysFont('Arial', BOARD_FONT_SIZE)
graph_font = pygame.font.SysFont('Arial', GRAPH_FONT_SIZE)
small_font = pygame.font.SysFont('Arial', GRAPH_FONT_SIZE - 2)

# Knight's possible moves (dx, dy)
MOVES = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]


def draw_knight(surface, x, y, size):
    knight_text = board_font.render("♘", True, BLACK)
    text_rect = knight_text.get_rect(center=(x, y))
    pygame.draw.circle(surface, (220, 220, 220), (x, y), size)
    surface.blit(knight_text, text_rect)


def is_valid(x, y, board):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == -1


def draw_chessboard(knight_pos, path, move_number):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color,
                             (CHESSBOARD_LEFT + col * SQUARE_SIZE,
                              CHESSBOARD_TOP + row * SQUARE_SIZE,
                              SQUARE_SIZE, SQUARE_SIZE))

    for i in range(1, len(path)):
        prev_x, prev_y = path[i - 1]
        curr_x, curr_y = path[i]
        pygame.draw.line(screen, PATH_COLOR,
                         (CHESSBOARD_LEFT + (prev_y + 0.5) * SQUARE_SIZE,
                          CHESSBOARD_TOP + (prev_x + 0.5) * SQUARE_SIZE),
                         (CHESSBOARD_LEFT + (curr_y + 0.5) * SQUARE_SIZE,
                          CHESSBOARD_TOP + (curr_x + 0.5) * SQUARE_SIZE), 3)

    for i, (x, y) in enumerate(path):
        # Use white text on black squares, black text on white squares
        text_color = WHITE if (x + y) % 2 != 0 else BLACK
        text = board_font.render(str(i + 1), True, text_color)
        text_rect = text.get_rect(center=(CHESSBOARD_LEFT + (y + 0.5) * SQUARE_SIZE,
                                          CHESSBOARD_TOP + (x + 0.5) * SQUARE_SIZE))
        screen.blit(text, text_rect)

    if knight_pos:
        kx, ky = knight_pos
        draw_knight(screen,
                    CHESSBOARD_LEFT + (ky + 0.5) * SQUARE_SIZE,
                    CHESSBOARD_TOP + (kx + 0.5) * SQUARE_SIZE,
                    SQUARE_SIZE // 3)


def draw_graph_visualization(path, current_step):
    white_nodes = []
    black_nodes = []

    # Collect all white and black squares
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 0:
                white_nodes.append((row, col))
            else:
                black_nodes.append((row, col))

    # Sort by row then column for better visualization
    white_nodes.sort(key=lambda x: (x[0], x[1]))
    black_nodes.sort(key=lambda x: (x[0], x[1]))

    # Draw white nodes (top row)
    for i, (row, col) in enumerate(white_nodes):
        x_pos = GRAPH_LEFT + i * GRAPH_NODE_SPACING
        y_pos = GRAPH_TOP

        # Draw square node
        pygame.draw.rect(screen, PURE_WHITE,
                         (x_pos - GRAPH_NODE_SIZE // 2, y_pos - GRAPH_NODE_SIZE // 2,
                          GRAPH_NODE_SIZE, GRAPH_NODE_SIZE))

        # Label above node
        label = f"{chr(ord('A') + col)}{row + 1}"
        label_text = graph_font.render(label, True, BLACK)
        text_width = label_text.get_width()
        screen.blit(label_text, (x_pos - text_width // 2, y_pos - 15))

        # Highlight if in path
        if (row, col) in path[:current_step + 1]:
            pygame.draw.rect(screen, PATH_COLOR,
                             (x_pos - GRAPH_NODE_SIZE // 2 + 1, y_pos - GRAPH_NODE_SIZE // 2 + 1,
                              GRAPH_NODE_SIZE - 2, GRAPH_NODE_SIZE - 2))
            step_text = small_font.render(str(path.index((row, col)) + 1), True, BLACK)
            screen.blit(step_text, (x_pos - step_text.get_width() // 2, y_pos - 6))

    # Draw black nodes (bottom row)
    for i, (row, col) in enumerate(black_nodes):
        x_pos = GRAPH_LEFT + i * GRAPH_NODE_SPACING
        y_pos = GRAPH_TOP + GRAPH_ROW_SPACING

        # Draw square node
        pygame.draw.rect(screen, PURE_BLACK,
                         (x_pos - GRAPH_NODE_SIZE // 2, y_pos - GRAPH_NODE_SIZE // 2,
                          GRAPH_NODE_SIZE, GRAPH_NODE_SIZE))

        # Label below node
        label = f"{chr(ord('A') + col)}{row + 1}"
        label_text = graph_font.render(label, True, BLACK)
        text_width = label_text.get_width()
        screen.blit(label_text, (x_pos - text_width // 2, y_pos + 15))

        # Highlight if in path
        if (row, col) in path[:current_step + 1]:
            pygame.draw.rect(screen, PATH_COLOR,
                             (x_pos - GRAPH_NODE_SIZE // 2 + 1, y_pos - GRAPH_NODE_SIZE // 2 + 1,
                              GRAPH_NODE_SIZE - 2, GRAPH_NODE_SIZE - 2))
            step_text = small_font.render(str(path.index((row, col)) + 1), True, WHITE)
            screen.blit(step_text, (x_pos - step_text.get_width() // 2, y_pos - 6))

    # Draw connections
    for i in range(1, current_step + 1):
        prev_row, prev_col = path[i - 1]
        curr_row, curr_col = path[i]

        prev_is_white = (prev_row + prev_col) % 2 == 0
        curr_is_white = (curr_row + curr_col) % 2 == 0

        if prev_is_white:
            prev_index = white_nodes.index((prev_row, prev_col))
            prev_x = GRAPH_LEFT + prev_index * GRAPH_NODE_SPACING
            prev_y = GRAPH_TOP
        else:
            prev_index = black_nodes.index((prev_row, prev_col))
            prev_x = GRAPH_LEFT + prev_index * GRAPH_NODE_SPACING
            prev_y = GRAPH_TOP + GRAPH_ROW_SPACING

        if curr_is_white:
            curr_index = white_nodes.index((curr_row, curr_col))
            curr_x = GRAPH_LEFT + curr_index * GRAPH_NODE_SPACING
            curr_y = GRAPH_TOP
        else:
            curr_index = black_nodes.index((curr_row, curr_col))
            curr_x = GRAPH_LEFT + curr_index * GRAPH_NODE_SPACING
            curr_y = GRAPH_TOP + GRAPH_ROW_SPACING

        pygame.draw.line(screen, GRAPH_LINE_COLOR, (prev_x, prev_y), (curr_x, curr_y), 1)


def knights_tour(start_x, start_y):
    board = [[-1 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    board[start_x][start_y] = 0
    path = [(start_x, start_y)]

    for step in range(1, BOARD_SIZE * BOARD_SIZE):
        x, y = path[-1]
        min_degree = BOARD_SIZE + 1
        next_move = None

        for dx, dy in MOVES:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, board):
                degree = 0
                for ndx, ndy in MOVES:
                    nnx, nny = nx + ndx, ny + ndy
                    if is_valid(nnx, nny, board):
                        degree += 1

                if degree < min_degree:
                    min_degree = degree
                    next_move = (nx, ny)

        if next_move is None:
            return False, path

        nx, ny = next_move
        board[nx][ny] = step
        path.append((nx, ny))

        screen.fill(BACKGROUND_COLOR)
        draw_chessboard((nx, ny), path, step)
        draw_graph_visualization(path, step)
        pygame.display.flip()
        pygame.time.delay(300)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    return True, path


def main():
    start_x, start_y = 0, 0
    success, path = knights_tour(start_x, start_y)

    if success:
        print("Knight's Tour Solution:")
        for i, (x, y) in enumerate(path):
            print(f"Step {i + 1}: {chr(ord('A') + y)}{x + 1}")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    else:
        print("No solution found")


if __name__ == "__main__":
    main()