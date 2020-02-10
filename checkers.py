#!C:\Users\Lee\AppData\Local\Programs\Python\Python38-32\python.exe
### Python AI Script
### Author: Lee Hughs
### Date: 2020/02/01

import sys

##initiate global variables/weights
p_weight = 2;
ep_weight = -2;
k_weight = 4;
ek_weight = -4;

class MoveTree:
    def __init__(self, src):
        self.moves = {
                0: src
                }
class Node:
    def __init__(self, board, player, move = None, parent = None):
        self.board = board
        #score = get_fitness(self.board)
        self.score = None
        self.player = player
        self.move = move
        self.parent = parent
        self.children = []

    #temp = Node(board, move)
    #temp.children.append(Node(board,move, temp))

def usage():
    print('''Script usage: checkers.py [board state as csv] [player as Rr:Bb] ''')


def mini_max(node, isMax, alpha, beta):
    if(len(node.children) == 0):
        return get_fitness(node.board)
    if(isMax):
        bestVal = float('-inf')
        for child in node.children:
            value = mini_max(child, False, alpha, beta)
            bestVal = max(bestVal, value)
            alpha = max(alpha, bestVal)
            if beta <= alpha:
                break
        node.score = bestVal
        return bestVal
    else:
        bestVal = float('inf')
        for child in node.children:
            value = mini_max(child, True, alpha, beta)
            bestVal = min(bestVal, value)
            beta = min(beta, bestVal)
            if(beta <= alpha):
                break
        node.score = bestVal
        return bestVal

#fill a tree with the possible board states/moves at "depth" moves from now
def fill_tree(root, depth):
    if(depth == 0):
        return
    moves = []
    enemy = ("Rr" if (root.player == "Bb") else "Bb")
   
    #enumerate through board looking for valid pieces to move
    for (i, row) in enumerate(root.board):
        for (j, value) in enumerate(row):
            if(str(value) in root.player):
                moves.extend(get_valid_moves(board, root.player, i, j))

    #populate root's children list
    for move in moves:
        root.children.append(Node(execute_move(root.board, move, root.player), enemy, move, root))

    #recursively call this method on all the children
    for child in root.children:
        fill_tree(child, depth-1)

#return a list of valid moves for a given piece
def get_valid_moves(board, player, i, j):
    moves = []
    #board = [row[:] for row in board_ref]  deep cloning not needed here
    dirx = ( 1 if (player == "Bb") else -1)

    #forward right check
    if(i + dirx >= 0 and i + dirx < 8 and j + 1 >= 0 and j + 1 < 8):
        if(board[i+dirx][j+1] == None):
            moves.append([[i,j],[i+dirx,j+1]])
    #forward left check
    if(i + dirx >= 0 and i + dirx < 8 and j - 1 >= 0 and j - 1 < 8):
        if(board[i+dirx][j-1] == None):
            moves.append([[i,j],[i+dirx,j-1]])

    #backwards checks
    if(str(board[i][j]) in "BR"):
        #backward right check
        if(i - dirx >= 0 and i - dirx < 8 and j + 1 >= 0 and j + 1 < 8):
            if(board[i-dirx][j+1] == None):
                moves.append([[i,j],[i-dirx,j+1]])
        #backward left check
        if(i - dirx >= 0 and i - dirx < 8 and j - 1 >= 0 and j - 1 < 8):
            if(board[i-dirx][j-1] == None):
                moves.append([[i,j],[i-dirx,j-1]])
    jumps = (get_valid_jumps(board, player, i, j))
    #clean jumps into solid paths
    for (k,jump) in enumerate(jumps):
        if (jump[0][0] == i and jump[0][1] == j):
            moves.append(jump)
        else:
            while(not(jump[0][0] == i and jump[0][1] == j)):
                for con_jump in reversed(jumps[:k]):
                    if(con_jump[1][0] == jump[0][0] and con_jump[1][1] == jump[0][1]):
                        jump.insert(0, con_jump[0])
                        break
            moves.append(jump)
    return moves

def get_valid_jumps(board_ref, player, i, j):
    jumps = []
    board = [row[:] for row in board_ref]
    dirx = ( 1 if (player == "Bb") else -1)
    enemy = ("Rr" if (player == "Bb") else "Bb")
    #forward right check
    if( i + (2*dirx) >= 0 and i + (2*dirx) < 8 and j + 2 >= 0 and j + 2 < 8):
        if( str(board[i+dirx][j+1]) in enemy and board[i+(2*dirx)][j+2] == None):
            jumps.append([[i,j],[i+(2*dirx),j+2]])
            board[i+dirx][j+1] = None
            jumps.extend(get_valid_jumps(board, player, i+(2*dirx), j+2))
    #forward left check
    if( i + (2*dirx) >= 0 and i + (2*dirx) < 8 and j - 2 >= 0 and j - 2 < 8):
        if( str(board[i+dirx][j-1]) in enemy and board[i+(2*dirx)][j-2] == None):
            jumps.append([[i,j],[i+(2*dirx),j-2]])
            board[i+dirx][j-1] = None
            jumps.extend(get_valid_jumps(board, player, i+(2*dirx), j-2))
    #backwards checks
    if(str(board[i][j]) in "BR"):
        dirx = dirx * -1
        #backwards right check
        if( i + (2*dirx) >= 0 and i + (2*dirx) < 8 and j + 2 >= 0 and j + 2 < 8):
            if( str(board[i+dirx][j+1]) in enemy and board[i+(2*dirx)][j+2] == None):
                jumps.append([[i,j],[i+(2*dirx),j+2]])
                board[i+dirx][j+1] = None
                jumps.extend(get_valid_jumps(board, player, i+(2*dirx), j+2))
        #backwards left check
        if( i + (2*dirx) >= 0 and i + (2*dirx) < 8 and j - 2 >= 0 and j - 2 < 8):
            if( str(board[i+dirx][j-1]) in enemy and board[i+(2*dirx)][j-2] == None):
                jumps.append([[i,j],[i+(2*dirx),j-2]])
                board[i+dirx][j-1] = None
                jumps.extend(get_valid_jumps(board, player, i+(2*dirx), j-2))

    return jumps;

#return a copy of board after executing a given move
def execute_move(board_ref, move, player):
    board = [row[:] for row in board_ref]
    if(abs(move[0][0] - move[1][0]) == 1 and abs(move[0][1] - move[1][1]) == 1):
        board[move[1][0]][move[1][1]] = board[move[0][0]][move[0][1]]
        board[move[0][0]][move[0][1]] = None
    else:
        for x in range(len(move)-1):
            board[(move[x][0] + move[x+1][0])//2][(move[x][1] + move[x+1][1])//2] = None
        board[move[len(move)-1][0]][move[len(move)-1][1]] = board[move[0][0]][move[0][1]]
        board[move[0][0]][move[0][1]] = None

    king_row = ( 0 if (player == "Rr") else 7)
    if(move[len(move)-1][0] == king_row):
        board[move[len(move)-1][0]][move[len(move)-1][1]] = board[move[len(move)-1][0]][move[len(move)-1][1]].upper()
    return board

#fitness fuinction for a given board state
def get_fitness(board, player = "Bb"):
    enemy = ("Rr" if (player == "Bb") else "Bb")
    score = float()
    for (i, row) in enumerate(board):
        for (j, value) in enumerate(row):
            ##square is empty
            if(value == None):
                continue
            #square has a piece
            if(value == player[1]):
                score += p_weight
                if(player == "Bb"):
                    score += (i+1)/8.0
                else:
                    score += (8-i)/8.0
                continue
            #square has a king
            if(value == player[0]):
                score += k_weight;
                continue
            #square has an enemy piece
            if(value == enemy[1]):
                score += ep_weight;
                if(enemy == "Bb"):
                    score -= (i+1)/8.0
                else:
                    score -= (8-i)/8.0
                continue
                #square has an enemy king
            if(value == enemy[0]):
                score += ek_weight;
    return score


#parse arguments, and start script
if __name__ == '__main__':
    #check the number of arguements is correct
    if(len(sys.argv) != 3):
        usage()
        exit(1)

    board = sys.argv[1].replace("\"","").split(",")
    #board = "b,null,b,null,b,null,b,null"
    #board += ",null,null,null,b,null,null,null,b"
    #board += ",b,null,b,null,b,null,b,null"
    #board += ",null,null,null,null,null,null,null,null,null,null,b,null,null,null,null,null"
    #board += ",null,r,null,r,null,r,null,r"
    #board += ",r,null,r,null,r,null,r,null"
    #board += ",null,r,null,r,null,r,null,r"
    #board = board.split(',')

    #change 1d array to 2d array
    board = [board[:8],board[8:16], board[16:24], board[24:32], board[32:40], board[40:48], board[48:56], board[56:64]]
    player = sys.argv[2]

    #change all instances of "null" string to None
    for (i, row) in enumerate(board):
        for (j, value) in enumerate(row):
            if(value == "null"):
                board[i][j] = None;

    root = Node(board, player)
    fill_tree(root, 5)
    
    score = mini_max(root, True, float('-inf'), float('inf'))
    move = None
    for child in root.children:
        if( child.score == score ):
            print(child.move)
            move = child
            break
    #for row in move.board:
        #print(row)




