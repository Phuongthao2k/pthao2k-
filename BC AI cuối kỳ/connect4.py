import numpy as np
import random
import pygame
import math
import time
import sys

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

EMPTY = 0
PLAYER_PIECE = -1
AI_PIECE = 1

WINDOW_LENGTH = 4

# Tạo bảng ROW_COUNT hàng, COLUMN_COUNT cột
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# Gán giá trị piece cho board[row][col]
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# KT hàng còn vt trống hay không
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

# Trả về vt trống nhỏ nhất trên hàng
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# In bảng ngược lại
def print_board(board):
    print(np.flip(board, 0))

# KT điều kiện thắng game
def winning_move(board, piece):
    # Kiểm tra vị trí hàng ngang để giành chiến thắng
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Kiểm tra vị trí hàng dọc để giành chiến thắng
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Kiểm tra đường chéo dốc tích cực
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Kiểm tra đường chéo dốc âm
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True

# Kt game đk kết thúc game
def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

# Trả về mảng các hàng còn trống trong bảng
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

# Hàm thao tác với pygame
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

# Trả về gt window
def evaluate_window(window, piece):
    score = 0
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    elif window.count(-piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

# Hàm đánh gía
def score_position(board, piece):
    score = 0
    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

# Trả về vị trí col cho giá trị lớn nhất
def pick_best_move(board, AI_Player):

	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, AI_Player)
		score = score_position(temp_board, AI_Player)
		if score > best_score:
			best_score = score
			best_col = col
	return best_col

# Thuật toán minimax
def minimax(board, depth, maximizingPlayer, AI_Player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_Player):
                return (None, 100000000000000)
            elif winning_move(board, -AI_Player):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_Player))

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_Player)
            new_score = minimax(b_copy, depth - 1, False, AI_Player)[1]
            if new_score > value:
                value = new_score
                column = col

        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, -AI_Player)
            new_score = minimax(b_copy, depth - 1, True, AI_Player)[1]
            if new_score < value:
                value = new_score
                column = col

        return column, value

# Thuật toán alpha-beta pruning
def alpha_beta(board, depth, alpha, beta, maximizingPlayer, AI_Player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_Player):
                return (None, 100000000000000)
            elif winning_move(board, -AI_Player):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_Player))

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_Player)
            new_score = alpha_beta(b_copy, depth - 1, alpha, beta, False, AI_Player)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, -AI_Player)
            new_score = alpha_beta(b_copy, depth - 1, alpha, beta, True, AI_Player)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

# Thuật toán negamax
def negamax(board, depth, alpha, beta, AI_Player, color):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_Player):
                return (None, color*100000000000000)
            elif winning_move(board, -AI_Player):
                return (None, -color*10000000000000)
            else:  # Game kết thúc mà không có người thắng
                return (None, 0)
        else:  # Depth is zero
            return (None, color*score_position(board, AI_Player))

    value = -math.inf
    column = random.choice(valid_locations)

    for col in valid_locations:
        row = get_next_open_row(board, col)
        b_copy = board.copy()
        drop_piece(b_copy, row, col, color)
        new_score = -negamax(b_copy, depth - 1, -beta, -alpha, AI_Player, -color)[1]
        if new_score > value:
            value = new_score
            column = col
        alpha = max(alpha, value)

        if alpha >= beta:
           break
    return column, value

# Thuật toán minmin
def minmin(board, depth, alpha, beta, AI_Player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_Player):
                return (None, 100000000000000)
            elif winning_move(board, -AI_Player):
                return (None, -10000000000000)
            else:  # Game kết thúc mà không có người thắng
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_Player))

    value = -math.inf
    column = random.choice(valid_locations)

    for col in valid_locations:
        row = get_next_open_row(board, col)
        b_copy = board.copy()
        drop_piece(b_copy, row, col, AI_Player)
        new_score = -minmin(b_copy, depth - 1, -beta, -alpha, -AI_Player)[1]
        if new_score > value:
            value = new_score
            column = col
        alpha = max(alpha, value)

        if alpha >= beta:
            break
    return column, value

# Thuật toán Expectimax
def expectimax(board, depth, alpha, beta, maximizingPlayer, AI_Player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_Player):
                return (None, 100000000000000)
            elif winning_move(board, -AI_Player):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_Player))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_Player)
            new_score = expectimax(b_copy, depth - 1, alpha, beta, False, AI_Player)[1]
            if new_score > value:
                value = new_score
                column = col

        return column, value

    else:
        depth_ = depth
        value = 0
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, -AI_Player)
            value += expectimax(b_copy, depth - 1, alpha, beta, True, AI_Player)[1]/len(valid_locations)
        a = math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, -AI_Player)
            new_score = abs(expectimax(b_copy, depth_ - 1, alpha, beta, AI_Player, 1)[1] - value)
            if new_score < a:
                a = new_score
                column = col

        return column, value

board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

count = 0
count_win = 0
avr_time = 0
i = 0

## Tạo vòng while để chơi game nhiều lần
while(i != 1):
    board = create_board()
    game_over = False
    turn = AI_PIECE

    while not game_over:

        ## Tạo đối thủ 1 là AI
        '''if turn == PLAYER_PIECE and not game_over:
            ## random
            #valid_locations = get_valid_locations(board)
            #col = random.choice(valid_locations)
            ## pick_best_move
            #col = pick_best_move(board, AI_PIECE)
            #col, alphabeta_score = minmin(board, 7,-math.inf, math.inf, PLAYER_PIECE)
            col, alphabeta_score = alpha_beta(board, 4, -math.inf, math.inf, True, PLAYER_PIECE)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)

                if winning_move(board, PLAYER_PIECE):
                    label = myfont.render("Player 1 wins!!", 1, RED)
                    screen.blit(label, (40, 10))
                    game_over = True

                if len(get_valid_locations(board)) == 0:
                    label = myfont.render("NO PLAYER WIN", 1, BLUE)
                    screen.blit(label, (40, 10))
                    game_over = True

                print_board(board)
                draw_board(board)
                turn = -turn'''

        ## Tạo đối thủ 1 là người chơi lựa chọn
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]

                if turn == PLAYER_PIECE:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

                # Người chơi
                if turn == PLAYER_PIECE:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                        turn = - turn

                        print_board(board)
                        draw_board(board)

        ## Tạo đối thủ 2 là AI
        if turn == AI_PIECE and not game_over:
            count += 1
            star_time = time.time()
            ## minimax
            #col, score = minimax(board, 3, True, AI_PIECE)
            # alpha_beta
            ##col,score = alpha_beta(board, 3, -math.inf, math.inf, True, AI_PIECE)
            ## negamax
            #col, score = negamax(board, 3, -math.inf, math.inf, AI_PIECE, AI_PIECE)
            ## expectimax
            #col, score = expectimax(board, 5, -math.inf, math.inf, True, AI_PIECE)
            ## minmin
            col, score = minmin(board, 4, -math.inf, math.inf, AI_PIECE)
            end_time = time.time()
            print("time: ", end_time - star_time)
            avr_time += (end_time - star_time)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    count_win += 1
                    label = myfont.render("Player 2 wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                if len(get_valid_locations(board)) == 0:
                    label = myfont.render("NO PLAYER WIN", 1, BLUE)
                    screen.blit(label, (40, 10))
                    game_over = True

                print_board(board)
                draw_board(board)

                turn = - turn

        if game_over:
            i += 1
            pygame.time.wait(3000)

print("win: ", count_win)
print("avr: ", count/i)
print("avr time: ", avr_time/count)

