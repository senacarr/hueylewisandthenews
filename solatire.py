import argparse
import os

class pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'X: {}, Y: {}'.format(self.x, self.y) 

class slot:
    is_selected = False
    is_current_pos = False
    def __init__(self, is_hole):
        self.is_hole = is_hole

###############################################################################################################
## Make Board
###############################################################################################################

def is_in_cross(idx):
    return idx > ROW_WIDTH - 1 and idx < 2 * ROW_WIDTH

def is_middle(x, y):
    return x == MIDDLE_IDX and y == MIDDLE_IDX

def make_board(size):
    return [[slot(is_middle(x, y) or not (is_in_cross(y) or is_in_cross(x))) for x in range(size)] for y in range(size)]

def clear_current_pos(board, size):
    for y in range(size):
        for x in range(size):
            board[x][y].is_current_pos = False

###############################################################################################################
## Make move
###############################################################################################################

def move(p, direction, number_hops):
    if not direction in DIRECTIONS:
        print 'Invalid direction: {}'.format(direction)

    return DIRECTIONS.get(direction, lambda p,n: p)(p,number_hops)

###############################################################################################################
## Check board
###############################################################################################################

def is_in_bounds(idx, size):
    return idx >= 0 and idx <= size

def is_valid_position(pos, size):
    return is_in_bounds(pos.x, size) and is_in_bounds(pos.y, size) and (is_in_cross(pos.x) or is_in_cross(pos.y))

def is_hole(board, pos):
    return board[pos.x][pos.y].is_hole

def is_position_selected(board, pos):
    return board[pos.x][pos.y].is_selected

def set_current_position(board, pos, is_current_pos):
    board[pos.x][pos.y].is_current_pos = is_current_pos
    return

def set_position_selected(board, pos, is_selected):
    board[pos.x][pos.y].is_selected = is_selected
    return

def set_is_hole(board, pos, is_hole):
    board[pos.x][pos.y].is_hole = is_hole
    return

###############################################################################################################
## Parse Args
###############################################################################################################

def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-s', '--size', default=9, help='size of the board')
    return arg_parser.parse_args()

def parse_input(ip, board, current_p, size):

    if ip == 'q':
        print 'Exiting'
        # print moves
        exit(0)

    current_pos = current_p
    if ip in DIRECTIONS:
        print 'Current Pos: {}'.format(str(current_pos))

        # if selected position, move marble
        if is_position_selected(board, current_pos):
            set_position_selected(board, current_pos, False)
            new_pos = move(current_pos, ip, 2)
            middle_pos = move(current_pos, ip, 1)
            print 'Middle Pos: {}'.format(str(middle_pos))

            if is_valid_position(new_pos, size) and is_hole(board, new_pos) and not is_hole(board, middle_pos):
                set_is_hole(board, middle_pos, True)
                set_is_hole(board, current_pos, True)
                current_pos = new_pos
                print 'Moved to: {}'.format(str(new_pos))
            else:
                print 'Invalid move\n'

        # if current position not selected find next marble in given direction
        else:
            new_pos = move(current_pos, ip, 1)
            if is_valid_position(new_pos, size) and not is_hole(board, new_pos):
                current_pos = new_pos
                print 'Set new current position to: {}\n'.format(str(new_pos))
            else:
                print 'Invalid move\n'

    elif ip == 'c':
        print 'Selected new position: {}\n\n'.format(str(current_pos))
        set_position_selected(board, current_pos, True)


    set_current_position(board, current_pos, True)
    set_is_hole(board, current_pos, False)
    
    print_board(board)

    return current_pos

###############################################################################################################
## Main
###############################################################################################################

def clear():
    os.system('clear')

def print_board(board):
    output = ''
    for y in range(size):
        for x in range(size):
            s = 'o' if board[x][y].is_hole else 'm'
            output += s.upper() if board[x][y].is_current_pos else s
            output += '\n' if x == size - 1 else ' '
    print output

if __name__ == '__main__':
    os.system('clear')

    print 'solataire v1\n\n'

    args = parse_args()
    size = args.size
    if size % 3 != 0 or size % 2 == 0:
        raise ValueError("Board width invalid, needs to be divisble by 3 and odd")

    global ROW_WIDTH
    ROW_WIDTH = size/3

    global MIDDLE_IDX
    MIDDLE_IDX = (size - 1)/2

    global DIRECTIONS
    DIRECTIONS = { 
        'w': lambda p, n: pos(p.x, p.y - n), # up
        's': lambda p, n: pos(p.x, p.y + n), # down
        'a': lambda p, n: pos(p.x - n, p.y), # left
        'd': lambda p, n: pos(p.x + n, p.y)  # right
    }

    start_position = pos(MIDDLE_IDX, MIDDLE_IDX - 2)

    print 'Start: {}'.format(str(start_position))

    current_pos = start_position

    board = make_board(size)
    board[current_pos.x][current_pos.y].is_current_pos = True
    print_board(board)

    while 1:
        clear_current_pos(board, size)
        move_dir = raw_input('Type a direction to move, c to CONFIRM, q to QUIT: ')
        os.system('clear')
        
        # parse input return current position if valid
        current_pos = parse_input(move_dir, board, current_pos, size)


    # os.system('clear')


#          Board
#
#   a  # # # x x x # # #
#   b  # # # x x x # # #
#   c  # # # x x x # # #
#   d  x x x x x x x x x
#   e  x x x x x x x x x
#   f  x x x x x x x x x
#   g  # # # x x x # # #
#   h  # # # x x x # # #
#   i  # # # x x x # # #
#      0 1 2 3 4 5 6 7 8


#    # # # # x x x x # # # # 
#    # # # # x x x x # # # #
#    # # # # x x x x # # # #
#    # # # # x x x x # # # #
#    x x x x x x x x x x x x
#    x x x x x x x x x x x x
#    x x x x x x x x x x x x
#    x x x x x x x x x x x x
#    # # # # x x x x # # # #
#    # # # # x x x x # # # #
#    # # # # x x x x # # # #
#    # # # # x x x x # # # # 


#     Try to calculate next valid marble
#     is_up = ip == 'w' or ip == 's'
#     is_positive = ip == 'w' or ip == 'd'
#     start_idx = current_pos.y if is_up else current_pos.x
#     end_idx = 0
#     
#     if is_positive:
#         end_idx = 2 * ROW_WIDTH if is_in_cross(current_pos.x if is_up else current_pos.y) else size - 1
#     else:
#         end_idx = ROW_WIDTH if is_in_cross(current_pos.x if is_up else current_pos.y) else 0
#     
#     for i in range(start_idx, size):
#         new_pos = move(current_pos, ip, 1)
#         if is_valid_position(new_pos, size) and not is_hole(new_pos):
#             current_pos = new_pos





