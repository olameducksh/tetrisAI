import pygame
import random

GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30

SCREEN_WIDTH = GRID_WIDTH * BLOCK_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * BLOCK_SIZE

black = (0, 0, 0)
grey = (65,68,67)
white = (181,181,182)

def create_grid():
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    return grid

def draw_grid_lines(surface):
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        pygame.draw.line(surface, grey, (x, 0), (x, SCREEN_HEIGHT))
    
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(surface, grey, (0,y), (SCREEN_WIDTH,y))
    
shape_dict = {
    'O_shape' : [
        [1, 1],
        [1, 1]
    ],

    'I_shape' : [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],

    'S_shape' : [
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0]
    ],

    'Z_shape' : [
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0]
    ],

    'L_shape' : [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 1]
    ],

    'J_shape' : [
        [0, 1, 0],
        [0, 1, 0],
        [1, 1, 0]
    ],

    'T_shape' : [
        [0, 0, 0],
        [1, 1, 1],
        [0, 1, 0]
    ],

}

color_dict = {
    'I_shape': (88,162,169),    # Cyan
    'J_shape': (55,82,251),      # Blue
    'L_shape': (204,135,0),    # Orange
    'O_shape': (188,182,27),    # Yellow
    'S_shape': (20,158,74),      # Green
    'T_shape': (142,36,136),    # Purple
    'Z_shape': (161,18,18)       # Red
}

class Block:
    def __init__(self,x,y,shape_name):
        self.x = x
        self.y = y
        self.shape = shape_dict[shape_name]
        self.color = color_dict[shape_name]
    
    def rotate(self):
        # rotate clockwise 90 degrees, first take transpose then reverse each row
        # debug: do not rotate in place as doing self.shape = ... made it reference, inplace will modify the shape-dict
        n = len(self.shape)
        new_matrix = [[0 for _ in range(n)] for _ in range(n)]

        for i in range(0, n):
            for j in range(0, n):
                new_matrix[j][n-1-i] = self.shape[i][j]
        
        self.shape = new_matrix
        
def draw_piece(surface, piece):
    for r in range(0, len(piece.shape)):
        for c in range(0, len(piece.shape[0])):
            if piece.shape[r][c] == 1:
                pixel_x = (piece.x + c) * BLOCK_SIZE
                pixel_y = (piece.y + r) * BLOCK_SIZE

                pygame.draw.rect(surface, piece.color, (pixel_x + 1,pixel_y +1 , BLOCK_SIZE-2, BLOCK_SIZE-2))
                pygame.draw.rect(surface, white, (pixel_x + 1,pixel_y+1, BLOCK_SIZE-2, BLOCK_SIZE-2), width= 1)

#draw the locked blocks on the board
def draw_board(surface, board):
    for r in range(0, GRID_HEIGHT):
        for c in range(0, GRID_WIDTH):
            if board[r][c] != 0:
                pixel_x = c*BLOCK_SIZE
                pixel_y = r*BLOCK_SIZE

                pygame.draw.rect(surface, board[r][c] , (pixel_x+1, pixel_y+1, BLOCK_SIZE-2, BLOCK_SIZE-2))


def lock_piece(piece, board):
    for r in range(0, len(piece.shape)):
        for c in range(0, len(piece.shape[0])):
            if piece.shape[r][c] == 1:
                temp_x = piece.x + c
                temp_y = piece.y + r
                board[temp_y][temp_x] = piece.color

def check_bounds(piece, board):
    #check if the block is within bounds, return false if not
    for r in range(0, len(piece.shape)):
        for c in range(0, len(piece.shape[0])):
            if piece.shape[r][c] == 1:
                temp_x = piece.x + c
                temp_y = piece.y + r

                if temp_x < 0 or temp_x >= GRID_WIDTH:
                    return False
                if temp_y >= GRID_HEIGHT:
                    return False
                if temp_y >= 0:
                    if board[temp_y][temp_x] != 0:
                        return False
    
    return True


def clear_lines(board):
    lines_cleared = 0
    r = GRID_HEIGHT - 1
    while r >= 0:                
        if 0 not in board[r]:
            # must delete this row and add a new row above
            del board[r]
            board.insert(0, [0 for _ in range(GRID_WIDTH)])
            lines_cleared += 1
        else:
            r -= 1

    return lines_cleared

def draw_ghost(surface, board, piece):
    original_y = piece.y
    while True:
        piece.y += 1
        if check_bounds(piece, board) == False:
            piece.y -= 1
            break
    
    ghost_y = piece.y

    piece.y = original_y

    for r in range(0, len(piece.shape)):
        for c in range(0, len(piece.shape[0])):
            if piece.shape[r][c] == 1:
                pixel_x = (piece.x + c) * BLOCK_SIZE
                pixel_y = (ghost_y + r) * BLOCK_SIZE

                pygame.draw.rect(surface, piece.color, (pixel_x+1,pixel_y+1, BLOCK_SIZE-2, BLOCK_SIZE-2), width= 1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    running = True
    clock = pygame.time.Clock()

    last_fall_time = pygame.time.get_ticks()
    fall_speed = 500 #half a second

    shape_list = list(shape_dict.keys())
    rand_block_no = random.randint(0,6)
    rand_block = shape_list[rand_block_no]
    current_block = Block(4,0, rand_block)

    main_board = create_grid()
    score = 0

    movingL = False
    movingR = False
    movingD = False
    slide_speed = 80
    last_move_time = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            #exit logic
            if event.type == pygame.QUIT:
                running = False
            #key press logic
            #simulate bound logic using "predict and revert" so change the posn but check if bounds after and revert if false
            if event.type == pygame.KEYDOWN:                
                # if event.key == pygame.K_LEFT:
                #     current_block.x = current_block.x - 1
                #     if(check_bounds(current_block, main_board) == False):
                #         current_block.x = current_block.x +1
                # if event.key == pygame.K_RIGHT:
                #     current_block.x = current_block.x + 1
                #     if(check_bounds(current_block, main_board) == False):
                #         current_block.x = current_block.x - 1
                # if event.key == pygame.K_DOWN:
                #     current_block.y = current_block.y + 1
                #     if(check_bounds(current_block, main_board) == False):
                #         current_block.y = current_block.y - 1
                if event.key == pygame.K_UP:
                    old_shape = current_block.shape
                    current_block.rotate()
                    if(check_bounds(current_block, main_board) == False):
                        current_block.shape = old_shape
                #hard drop
                if event.key == pygame.K_z:
                    while True:
                        current_block.y = current_block.y + 1
                        if check_bounds(current_block, main_board) == False:
                            current_block.y -= 1
                            break
                
                if event.key == pygame.K_LEFT:
                    movingL = True
                if event.key == pygame.K_RIGHT:
                    movingR = True
                if event.key == pygame.K_DOWN:
                    movingD = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    movingL = False
                if event.key == pygame.K_RIGHT:
                    movingR = False
                if event.key == pygame.K_DOWN:
                    movingD = False        

        current_time = pygame.time.get_ticks()
        #move logic
        if current_time - last_move_time > slide_speed:
            if movingL:
                current_block.x = current_block.x - 1
                if(check_bounds(current_block, main_board) == False):
                    current_block.x = current_block.x +1
            if movingR:
                current_block.x = current_block.x + 1
                if(check_bounds(current_block, main_board) == False):
                    current_block.x = current_block.x - 1
            if movingD:
                current_block.y = current_block.y + 1
                if(check_bounds(current_block, main_board) == False):
                    current_block.y = current_block.y - 1

            last_move_time = current_time

        #gravity logic
        if current_time - last_fall_time > fall_speed:
            current_block.y = current_block.y + 1
            if(check_bounds(current_block, main_board) == False):
                current_block.y = current_block.y - 1
                lock_piece(current_block, main_board)
                lines_cleared = clear_lines(main_board)

                if lines_cleared > 0:
                    score += lines_cleared*100
                    print("score: ", score)

                # get new random block each time
                shape_list = list(shape_dict.keys())
                rand_block_no = random.randint(0,6)
                rand_block = shape_list[rand_block_no]
                current_block = Block(4,0, rand_block)

                # death check
                if check_bounds(current_block, main_board) == False:
                    print("game over type shit")
                    running = False

            last_fall_time = current_time

        #create screen and grid
        screen.fill("black")
        draw_grid_lines(surface=screen)

        #draw the board with locked pieces
        draw_board(screen, main_board)
        #create piece
        draw_ghost(screen, main_board, current_block)
        draw_piece(screen, current_block)

        pygame.display.flip()
        clock.tick(60) #refresh rate = 60

    pygame.quit()

if __name__ == "__main__":
    main()