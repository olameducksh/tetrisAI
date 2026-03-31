import copy
GRID_WIDTH = 10
GRID_HEIGHT = 20

WEIGHT_LINES = 3.4
WEIGHT_HEIGHT = -0.51
WEIGHT_HOLES = -0.36
WEIGHT_BUMPINESS = -0.18

def calculate_score(board, lines_cleared):
    height = agg_height(board)
    holes = count_holes(board)
    bumpiness = get_bumpiness(board)
    score = (lines_cleared * WEIGHT_LINES) + (height * WEIGHT_HEIGHT) + (holes * WEIGHT_HOLES) + (bumpiness * WEIGHT_BUMPINESS)
    return score

#param 1: how many lines are completed with this exact step
def completed_line(baord):
    lines = 0
    for r in range(0, GRID_HEIGHT):
        if 0 not in baord[r]:
            lines += 1
    
    return lines

#param 2: aggregate height: how tall is the tower (we want this to be small)
def agg_height(board):
    total_h = 0
    for c in range(0, GRID_WIDTH):
        for r in range(GRID_HEIGHT):
            if board[r][c] != 0:
                temp = GRID_HEIGHT - r
                total_h += temp
                break
            
    return total_h

#param 3: no of holes (holes = bad)
def count_holes(board):
    total_holes = 0
    for c in range(GRID_WIDTH):
        block_found = False
        for r in range(GRID_HEIGHT):
            if board[r][c] != 0:
                block_found = True #we at roof of the stack
            elif board[r][c] == 0 and block_found:
                # empty space underneath the block
                total_holes += 1
    return total_holes

#param 4: bumpiness (we dont want one column to be bigger than others)
def get_bumpiness(board):
    # sum of all adjacent column heights
    total_bump = 0
    height_A = GRID_HEIGHT
    for i in range(0, GRID_HEIGHT):
        if board[i][0] != 0:
            height_A = i
            break
    
    for c in range(1, GRID_WIDTH):
        height_B = GRID_HEIGHT

        for r in range(0, GRID_HEIGHT):
            if board[r][c] != 0:
                height_B = r
                break
        
        total_bump += abs(height_B - height_A)
        height_A = height_B

    return total_bump

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


#now we try all possible rotations from all possible positions to get best move on a copied board..
def get_best_move(board, piece):
    best_score = -999999
    bestX = 4
    bestRotation = 0
    base_piece = copy.deepcopy(piece)
 
    for rotation in range(0, 4):
        rotated_piece = copy.deepcopy(base_piece)
        for _ in range(rotation):
            rotated_piece.rotate()
 
        for x in range(-2, GRID_WIDTH):
            copy_board = copy.deepcopy(board)
            copy_piece = copy.deepcopy(rotated_piece)
            copy_piece.x = x
            copy_piece.y = 0
 
            if check_bounds(copy_piece, copy_board) == False:
                continue
 
            while check_bounds(copy_piece, copy_board) == True:
                copy_piece.y += 1
            copy_piece.y -= 1
 
            lock_piece(copy_piece, copy_board)
            lines = completed_line(copy_board) # counted after locking
            temp_score = calculate_score(copy_board, lines)
            if temp_score > best_score:
                best_score = temp_score
                bestX = x
                bestRotation = rotation
 
    return best_score, bestX, bestRotation