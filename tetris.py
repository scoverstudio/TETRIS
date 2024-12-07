import pygame
import random

pygame.init()

WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLUMNS = WIDTH // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE
SIDE_PANEL_WIDTH = 200 
TOTAL_WIDTH = WIDTH + SIDE_PANEL_WIDTH 

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
COLORS = [
    (0, 255, 255),  
    (255, 165, 0),  
    (0, 0, 255),    
    (255, 255, 0),  
    (0, 255, 0),   
    (255, 0, 0),   
    (128, 0, 128), 
]

SHAPES = [
    [[  
        [1, 1, 1, 1]
    ], [
        [1],
        [1],
        [1],
        [1]
    ]],
    [[  
        [1, 1],
        [1, 1]
    ]],
    [[  
        [0, 1, 0],
        [1, 1, 1]
    ], [
        [1, 0],
        [1, 1],
        [1, 0]
    ], [
        [1, 1, 1],
        [0, 1, 0]
    ], [
        [0, 1],
        [1, 1],
        [0, 1]
    ]],
    [[  
        [1, 0, 0],
        [1, 1, 1]
    ], [
        [1, 1],
        [1, 0],
        [1, 0]
    ], [
        [1, 1, 1],
        [0, 0, 1]
    ], [
        [0, 1],
        [0, 1],
        [1, 1]
    ]],
    [[  
        [0, 0, 1],
        [1, 1, 1]
    ], [
        [1, 0],
        [1, 0],
        [1, 1]
    ], [
        [1, 1, 1],
        [1, 0, 0]
    ], [
        [1, 1],
        [0, 1],
        [0, 1]
    ]],
    [[  
        [1, 1, 0],
        [0, 1, 1]
    ], [
        [0, 1],
        [1, 1],
        [1, 0]
    ]],
    [[  
        [0, 1, 1],
        [1, 1, 0]
    ], [
        [1, 0],
        [1, 1],
        [0, 1]
    ]]
]

screen = pygame.display.set_mode((TOTAL_WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

font = pygame.font.SysFont('comicsans', 30)

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

    def get_blocks(self):
        rotated_shape = self.shape[self.rotation]
        return rotated_shape

def create_grid(locked_positions):
    grid = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]
    for (x, y), color in locked_positions.items():
        if 0 <= y < ROWS and 0 <= x < COLUMNS:
            grid[y][x] = color
    return grid

def draw_grid(grid):
    for i in range(ROWS):
        for j in range(COLUMNS):
            pygame.draw.rect(screen, grid[i][j], (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, GRAY, (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_piece(piece):
    blocks = piece.get_blocks()
    for i, row in enumerate(blocks):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, piece.color, 
                                 ((piece.x + j) * BLOCK_SIZE, 
                                  (piece.y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def valid_space(piece, grid):
    formatted = convert_shape_format(piece)
    for pos in formatted:
        x, y = pos
        if x < 0 or x >= COLUMNS or y >= ROWS:
            return False
        if y >= 0 and grid[y][x] != BLACK:
            return False
    return True

def convert_shape_format(piece):
    positions = []
    blocks = piece.get_blocks()
    for i, row in enumerate(blocks):
        for j, cell in enumerate(row):
            if cell:
                positions.append((piece.x + j, piece.y + i))
    return positions

def clear_rows(grid, locked_positions):
    cleared_rows = 0
    for i in range(ROWS - 1, -1, -1):
        if BLACK not in grid[i]:
            cleared_rows += 1
            for x in range(COLUMNS):
                if (x, i) in locked_positions:
                    del locked_positions[(x, i)]

    if cleared_rows > 0:
        for y in range(ROWS - 1, -1, -1):
            for x in range(COLUMNS):
                if (x, y) in locked_positions:
                    new_y = y + cleared_rows
                    if new_y < ROWS:
                        locked_positions[(x, new_y)] = locked_positions.pop((x, y))
    return cleared_rows


def del_row(locked_positions, row):
    for (x, y) in list(locked_positions.keys()):
        if y == row:
            del locked_positions[(x, y)]
        elif y < row:
            locked_positions[(x, y + 1)] = locked_positions.pop((x, y))

def draw_text(text, x, y):
    label = font.render(text, True, WHITE)
    screen.blit(label, (x, y))

def draw_sidebar(hold_piece, next_piece):
    x_offset = WIDTH + 20
    y_offset = 50

    label = font.render("Hold", True, WHITE)
    screen.blit(label, (x_offset, y_offset))
    if hold_piece is not None:
        blocks = hold_piece.get_blocks()
        for i, row in enumerate(blocks):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, hold_piece.color,
                                     (x_offset + j * BLOCK_SIZE, y_offset + 40 + i * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))

    y_offset += 200
    label = font.render("Next Figure", True, WHITE)
    screen.blit(label, (x_offset, y_offset))
    blocks = next_piece.get_blocks()
    for i, row in enumerate(blocks):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, next_piece.color,
                                 (x_offset + j * BLOCK_SIZE, y_offset + 40 + i * BLOCK_SIZE,
                                  BLOCK_SIZE, BLOCK_SIZE))

def draw_menu():
    screen.fill(BLACK)
    
    title_font = pygame.font.SysFont('comicsans', 50)
    title = title_font.render("TETRIS", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
    
    button_font = pygame.font.SysFont('comicsans', 40)
    start_button = button_font.render("START", True, WHITE)
    start_rect = pygame.Rect(WIDTH // 2 - start_button.get_width() // 2 - 10, 250, start_button.get_width() + 20, 50)
    pygame.draw.rect(screen, GRAY, start_rect)
    screen.blit(start_button, (start_rect.x + 10, start_rect.y + 5))
    
    controls_font = pygame.font.SysFont('comicsans', 25)
    controls = [
        "Controls:",
        "Arrow keys to move",
        "Up to rotate",
        "Down to speed up",
        "C to hold piece",
        "Hold Left/Right to speed movement"
    ]
    y_offset = HEIGHT - 150
    for line in controls:
        text = controls_font.render(line, True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 30
    
    return start_rect


def menu():
    while True:
        start_rect = draw_menu()
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    main()

def main():
    locked_positions = {}
    grid = create_grid(locked_positions)
    current_piece = Piece(5, 0, random.choice(SHAPES))
    next_piece = Piece(5, 0, random.choice(SHAPES))
    hold_piece = None
    hold_used = False
    score = 0
    level = 1
    time_elapsed = 0
    run = True
    fall_time = 0

    left_key_hold_time = 0
    right_key_hold_time = 0
    is_left_boost_active = False
    is_right_boost_active = False
    move_interval = 200
    last_move_time = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        time_elapsed += clock.get_rawtime()
        clock.tick()

        fall_speed = max(50, 500 - (level - 1) * 50)

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            fall_speed = 50

        if fall_time / fall_speed > 1:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                for pos in convert_shape_format(current_piece):
                    locked_positions[pos] = current_piece.color
                cleared = clear_rows(grid, locked_positions)
                score += cleared ** 2 * 100
                current_piece = next_piece
                next_piece = Piece(5, 0, random.choice(SHAPES))
                hold_used = False
                left_key_hold_time = 0
                right_key_hold_time = 0
                is_left_boost_active = False
                is_right_boost_active = False

        if time_elapsed >= 20000:
            level += 1
            time_elapsed = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if left_key_hold_time == 0:
                        left_key_hold_time = pygame.time.get_ticks()
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    if right_key_hold_time == 0:
                        right_key_hold_time = pygame.time.get_ticks()
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
                if event.key == pygame.K_c and not hold_used:
                    if hold_piece is None:
                        hold_piece = current_piece
                        current_piece = next_piece
                        next_piece = Piece(5, 0, random.choice(SHAPES))
                    else:
                        hold_piece, current_piece = current_piece, hold_piece
                    current_piece.x, current_piece.y = 5, 0
                    hold_used = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left_key_hold_time = 0
                    is_left_boost_active = False
                if event.key == pygame.K_RIGHT:
                    right_key_hold_time = 0
                    is_right_boost_active = False

        current_time = pygame.time.get_ticks()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            if left_key_hold_time > 0 and (current_time - left_key_hold_time > 500):
                is_left_boost_active = True
                if current_time - last_move_time > move_interval:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                    last_move_time = current_time
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if right_key_hold_time > 0 and (current_time - right_key_hold_time > 500):
                is_right_boost_active = True
                if current_time - last_move_time > move_interval:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                    last_move_time = current_time

        cleared = clear_rows(grid, locked_positions)
        if cleared > 0:
            score += cleared ** 2 * 100

        screen.fill(BLACK)
        draw_grid(grid)
        draw_piece(current_piece)
        draw_sidebar(hold_piece, next_piece)
        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"Level: {level}", 10, 40)
        pygame.display.update()

        if any(y < 1 for (x, y) in locked_positions):
            run = False

    menu()

if __name__ == "__main__":
    menu()
    main()