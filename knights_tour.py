# -------------------------------------------------------------------------------------
# Fadil Eldin
# July 12 2025
# Knight's Tour Visualization with Stop/Resume and Speed Control
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
# from collections import deque
# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1300, 800
BOARD_SIZE = 8
SQUARE_SIZE = 70
CHESSBOARD_LEFT = (WIDTH - BOARD_SIZE * SQUARE_SIZE) // 2
CHESSBOARD_TOP = 20
GRAPH_TOP = CHESSBOARD_TOP + BOARD_SIZE * SQUARE_SIZE + 60
GRAPH_LEFT = 40
GRAPH_NODE_SPACING = 40
GRAPH_NODE_SIZE = 15
BACKGROUND_COLOR = (240, 217, 181)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
PURE_WHITE = (255, 255, 255)
PURE_BLACK = (0, 0, 0)
PATH_COLOR = (50, 200, 50)
FONT_COLOR = (0, 0, 0)
BOARD_FONT_SIZE = 20
SCORE_FONT_SIZE = 14  # Smaller font for scores
GRAPH_FONT_SIZE = 12
GRAPH_LINE_COLOR = (100, 100, 100)
GRAPH_ROW_SPACING = 100
LABEL_VERTICAL_OFFSET = 25
KNIGHT_COLOR = (50, 50, 200)
# CONTROL_PANEL_COLOR = (220, 220, 220)
CONTROL_PANEL_COLOR = YELLOW
CONTROL_PANEL_PADDING = 10
WHITE_SQUARE_SCORE_COLOR = (200, 0, 0)  # Red for white squares
BLACK_SQUARE_SCORE_COLOR = (255, 255, 0)  # Yellow for black squares

# Animation speed (global variable)
ANIMATION_SPEED = 1000  # milliseconds
paused = False

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Knight's Tour - Warnsdorff's Rule Visualization")
board_font = pygame.font.SysFont('Arial', BOARD_FONT_SIZE)
score_font = pygame.font.SysFont('Arial', SCORE_FONT_SIZE)
graph_font = pygame.font.SysFont('Arial', GRAPH_FONT_SIZE)
small_font = pygame.font.SysFont('Arial', GRAPH_FONT_SIZE - 2)
control_font = pygame.font.SysFont('Arial', 16)

# Knight's possible moves (dx, dy)
MOVES = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]
# -------------------------------------------------------------------------------------
def draw_control_panel():
    """Draws the control panel at the top left"""
    panel_width = 300
    panel_height = 80
    pygame.draw.rect(screen, CONTROL_PANEL_COLOR,
                     (CONTROL_PANEL_PADDING, CONTROL_PANEL_PADDING,
                      panel_width, panel_height))

    # Draw controls text
    controls = [
        "SPACE: Pause/Resume",
        "UP/DOWN: Speed +/- 100ms",
        f"Current Speed: {ANIMATION_SPEED}ms"
    ]

    for i, text in enumerate(controls):
        text_surface = control_font.render(text, True, BLACK)
        screen.blit(text_surface,
                    (CONTROL_PANEL_PADDING + 10,
                     CONTROL_PANEL_PADDING + 10 + i * 20))
# -------------------------------------------------------------------------------------
def chess_coords(row, col):
    """Convert matrix indices to chess notation (A1-H8)"""
    return f"{chr(ord('A') + col)}{BOARD_SIZE - row}"

# -------------------------------------------------------------------------------------
def draw_knight(surface, x, y, size):
    knight_text = board_font.render("♘", True, YELLOW)
    text_rect = knight_text.get_rect(center=(x, y))
    pygame.draw.circle(surface, KNIGHT_COLOR, (x, y), size)
    surface.blit(knight_text, text_rect)

# -------------------------------------------------------------------------------------
def is_valid(x, y, board):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == -1
# -------------------------------------------------------------------------------------
def count_possible_moves(x, y, board):
    """Count how many valid moves are available from (x,y)"""
    count = 0
    for dx, dy in MOVES:
        nx, ny = x + dx, y + dy
        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:  # Just check bounds
            if board[nx][ny] == -1:  # Only count unvisited squares
                count += 1
    return count
# -------------------------------------------------------------------------------------
def draw_chessboard_coordinates():
    # Draw letters (A-H) below the board (left to right)
    for col in range(BOARD_SIZE):
        letter = chr(ord('A') + col)
        # text = small_font.render(letter, True, BLACK)
        text = board_font.render(letter, True, BLACK)
        screen.blit(text, (CHESSBOARD_LEFT + col * SQUARE_SIZE + SQUARE_SIZE // 2 - text.get_width() // 2,
                           CHESSBOARD_TOP + BOARD_SIZE * SQUARE_SIZE + 5))

    # Draw numbers (1-8) to the left of the board - 1 at bottom, 8 at top
    for row in range(BOARD_SIZE):
        number = str(row + 1)  # 1 to 8 from bottom to top
        # text = small_font.render(number, True, BLACK)
        text = board_font.render(number, True, BLACK)
        y_pos = CHESSBOARD_TOP + (BOARD_SIZE - row - 1) * SQUARE_SIZE + SQUARE_SIZE // 2 - text.get_height() // 2
        screen.blit(text, (CHESSBOARD_LEFT - 20, y_pos))
# -------------------------------------------------------------------------------------
def draw_chessboard(knight_pos, path, board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            is_white = (row + col) % 2 == 0
            color = WHITE if is_white else BLACK
            pygame.draw.rect(screen, color,
                           (CHESSBOARD_LEFT + col * SQUARE_SIZE,
                            CHESSBOARD_TOP + row * SQUARE_SIZE,
                            SQUARE_SIZE, SQUARE_SIZE))

            # Always draw move scores for all squares (modified this part)
            moves_count = count_possible_moves(row, col, board)
            if moves_count >= 0:  # Show for all squares, even visited ones
                score_color = WHITE_SQUARE_SCORE_COLOR if is_white else BLACK_SQUARE_SCORE_COLOR
                score_text = score_font.render(str(moves_count), True, score_color)
                score_rect = score_text.get_rect(
                    topleft=(CHESSBOARD_LEFT + col * SQUARE_SIZE + 5,
                            CHESSBOARD_TOP + row * SQUARE_SIZE + 5))
                screen.blit(score_text, score_rect)

    # Rest of the function remains the same...
    # Draw path lines
    for i in range(1, len(path)):
        prev_x, prev_y = path[i - 1]
        curr_x, curr_y = path[i]
        pygame.draw.line(screen, PATH_COLOR,
                         (CHESSBOARD_LEFT + (prev_y + 0.5) * SQUARE_SIZE,
                          CHESSBOARD_TOP + (prev_x + 0.5) * SQUARE_SIZE),
                         (CHESSBOARD_LEFT + (curr_y + 0.5) * SQUARE_SIZE,
                          CHESSBOARD_TOP + (curr_x + 0.5) * SQUARE_SIZE), 3)

    # Draw move numbers in center
    for i, (x, y) in enumerate(path):
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

    draw_chessboard_coordinates()
# -------------------------------------------------------------------------------------
def draw_graph_visualization(path, current_step):
    white_nodes = []
    black_nodes = []

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 0:
                white_nodes.append((row, col))
            else:
                black_nodes.append((row, col))

    white_nodes.sort(key=lambda x: (x[0], x[1]))
    black_nodes.sort(key=lambda x: (x[0], x[1]))

    # Draw white nodes (top row)
    for i, (row, col) in enumerate(white_nodes):
        x_pos = GRAPH_LEFT + i * GRAPH_NODE_SPACING
        y_pos = GRAPH_TOP

        pygame.draw.rect(screen, PURE_WHITE,
                         (x_pos - GRAPH_NODE_SIZE // 2, y_pos - GRAPH_NODE_SIZE // 2,
                          GRAPH_NODE_SIZE, GRAPH_NODE_SIZE))

        label = chess_coords(row, col)
        label_text = graph_font.render(label, True, BLACK)
        text_width = label_text.get_width()
        screen.blit(label_text, (x_pos - text_width // 2, y_pos - LABEL_VERTICAL_OFFSET))

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

        pygame.draw.rect(screen, PURE_BLACK,
                         (x_pos - GRAPH_NODE_SIZE // 2, y_pos - GRAPH_NODE_SIZE // 2,
                          GRAPH_NODE_SIZE, GRAPH_NODE_SIZE))

        label = chess_coords(row, col)
        label_text = graph_font.render(label, True, BLACK)
        text_width = label_text.get_width()
        screen.blit(label_text, (x_pos - text_width // 2, y_pos + LABEL_VERTICAL_OFFSET))

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

# -------------------------------------------------------------------------------------
def knights_tour(start_x, start_y):
    global ANIMATION_SPEED, paused

    board = [[-1 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    board[start_x][start_y] = 0
    path = [(start_x, start_y)]

    for step in range(1, BOARD_SIZE * BOARD_SIZE):
        x, y = path[-1]
        min_degree = BOARD_SIZE + 1
        next_move = None

        # Find all possible next moves
        possible_moves = []
        for dx, dy in MOVES:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, board):
                degree = count_possible_moves(nx, ny, board)
                possible_moves.append((degree, nx, ny))

                if degree < min_degree:
                    min_degree = degree
                    next_move = (nx, ny)

        if next_move is None:
            return False, path

        nx, ny = next_move
        board[nx][ny] = step
        path.append((nx, ny))

        # Handle events and controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_UP:
                    ANIMATION_SPEED = max(100, ANIMATION_SPEED - 100)
                elif event.key == pygame.K_DOWN:
                    ANIMATION_SPEED += 100

        # Draw everything
        screen.fill(BACKGROUND_COLOR)
        draw_control_panel()
        draw_chessboard((nx, ny), path, board)
        draw_graph_visualization(path, step)
        pygame.display.flip()

        # Handle pause
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                    elif event.key == pygame.K_UP:
                        ANIMATION_SPEED = max(100, ANIMATION_SPEED - 100)
                    elif event.key == pygame.K_DOWN:
                        ANIMATION_SPEED += 100

            # Update control panel while paused
            screen.fill(BACKGROUND_COLOR)
            draw_control_panel()
            draw_chessboard((nx, ny), path, board)
            draw_graph_visualization(path, step)
            pygame.display.flip()
            pygame.time.delay(100)

        pygame.time.delay(ANIMATION_SPEED)

    return True, path
# -------------------------------------------------------------------------------------
def main():
    global ANIMATION_SPEED, paused

    # Start at A8 (top-left corner in chess notation)
    start_x, start_y = 0, 0
    success, path = knights_tour(start_x, start_y)

    if success:
        print("\nKnight's Tour Completed!")
        for i, (x, y) in enumerate(path):
            print(f"Step {i + 1}: {chess_coords(x, y)}")

        # Keep window open after completion
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Allow restarting after completion
                        main()
                        return
    else:
        print("No solution found")
# -------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
# -------------------------------------------------------------------------------------
