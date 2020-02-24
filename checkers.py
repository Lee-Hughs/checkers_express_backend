#!/usr/bin/python3.5
### Python AI Script
### Author: Lee Hughs
### Date: 2020/02/01

import sys
import json
import random
##initiate global variables/weights
p_weight = 1;
ep_weight = -1;
k_weight = 2;
ek_weight = -2;

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

class Brain:
    def __init__(self, player, weights):
        self.player = player
        self.weights = weights

def usage():
    print('''Script usage: checkers.py [board state as csv] [player as Rr:Bb] ''')


def mini_max(node, brain, isMax, alpha, beta):
    if(len(node.children) == 0):
        node.score = get_fitness(node.board, brain, brain.player)
        return node.score
    if(isMax):
        bestVal = float('-inf')
        for child in node.children:
            value = mini_max(child, brain, False, alpha, beta)
            bestVal = max(bestVal, value)
            alpha = max(alpha, bestVal)
            if beta <= alpha:
                break
        node.score = bestVal
        return bestVal
    else:
        bestVal = float('inf')
        for child in node.children:
            value = mini_max(child, brain, True, alpha, beta)
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
                moves.extend(get_valid_moves(root.board, root.player, i, j))

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
            temp = [square[:] for square in jump]
            while(not(temp[0][0] == i and temp[0][1] == j)):
                for con_jump in reversed(jumps[:k]):
                    if(con_jump[1][0] == temp[0][0] and con_jump[1][1] == temp[0][1]):
                        temp.insert(0, con_jump[0])
                        if(temp[0][0] == i and temp[0][1] == j):
                            break
            moves.append(temp)
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
    king_row = ( 0 if (player == "Rr") else 7)
    board = [row[:] for row in board_ref]
    if(abs(move[0][0] - move[1][0]) == 1 and abs(move[0][1] - move[1][1]) == 1):
        board[move[1][0]][move[1][1]] = board[move[0][0]][move[0][1]]
        board[move[0][0]][move[0][1]] = None
    else:
        for x in range(len(move)-1):
            board[(move[x][0] + move[x+1][0])//2][(move[x][1] + move[x+1][1])//2] = None
        board[move[len(move)-1][0]][move[len(move)-1][1]] = board[move[0][0]][move[0][1]]
        board[move[0][0]][move[0][1]] = None

    if(move[len(move)-1][0] == king_row):
        board[move[len(move)-1][0]][move[len(move)-1][1]] = board[move[len(move)-1][0]][move[len(move)-1][1]].upper()
    return board

#fitness fuinction for a given board state
def get_fitness(board, brain, player = "Bb"):
    enemy = ("Rr" if (player == "Bb") else "Bb")
    score = float()
    score += get_pawn_score(board, player, brain.weights[0])
    score += get_king_score(board, player, brain.weights[1])
    score += get_safe_pawn(board, player, brain.weights[2])
    score += get_safe_king(board, player, brain.weights[3])
    score += get_m_pawns(board, player, brain.weights[4])
    score += get_m_kings(board, player, brain.weights[5])
    score += get_p_distance(board, player, brain.weights[6])
    score += get_p_spots(board, player, brain.weights[7])
    score += get_defenders(board, player, brain.weights[8])
    return score

def get_pawn_score(board, player, w):
    score = 0
    enemy = ("Rr" if (player == "Bb") else "Bb")
    for (i, row) in enumerate(board):
        for (j, value) in enumerate(row):
            ##square is empty
            if(value == None):
                continue
            #square has a piece
            if(value == player[1]):
                score += w
                continue
            if(value == enemy[1]):
                score -= w
    return score

def get_king_score(board, player, w):
    score = 0
    enemy = ("Rr" if (player == "Bb") else "Bb")
    for (i, row) in enumerate(board):
        for (j, value) in enumerate(row):
            ##square is empty
            if(value == None):
                continue
            #square has a piece
            if(value == player[0]):
                score += w
                continue
            if(value == enemy[0]):
                score -= w
    return score

def get_safe_pawn(board, player, w):
    score = 0
    enemy = ("Rr" if (player == "Bb") else "Bb")
    for (i, row) in enumerate(board):
        if(row[0] == player[1]):
            score += w
        if(row[0] == enemy[1]):
            score -= w
        if(row[7] == player[1]):
            score += w
        if(row[7] == enemy[1]):
            score -= w
    return score

def get_safe_king(board, player, w):
    score = 0
    enemy = ("Rr" if (player == "Bb") else "Bb")
    for (i, row) in enumerate(board):
        if(row[0] == player[0]):
            score += w
        if(row[0] == enemy[0]):
            score -= w
        if(row[7] == player[0]):
            score += w
        if(row[7] == enemy[0]):
            score -= w
    return score
def get_m_pawns(board, player, w):
    score = 0
    enemy = ("Rr" if (player == "Bb") else "Bb")
    for (i, row) in enumerate(board):
        for (j, value) in enumerate(row):
            if(value == None):
                continue
            if(value == player[1]):
                if(len(get_valid_moves(board, player, i, j)) != 0):
                    score += w
                    continue
            if(value == enemy[1]):
                if(len(get_valid_moves(board, enemy, i, j)) != 0):
                    score -= w
                    continue
    return score

def get_m_kings(board, player, w):
    score = 0
    enemy = ("Rr" if (player == "Bb") else "Bb")
    for (i, row) in enumerate(board):
        for (j, value) in enumerate(row):
            if(value == None):
                continue
            if(value == player[0]):
                if(len(get_valid_moves(board, player, i, j)) != 0):
                    score += w
                    continue
            if(value == enemy[0]):
                if(len(get_valid_moves(board, enemy, i, j)) != 0):
                    score -= w
                    continue
    return score
def get_p_distance(board, player, w):
    score = 0
    for (i, row) in enumerate(board):
        for (j, value) in enumerate(row):
            if(value == None):
                continue
            if(value == player[1]):
                if(player == 'Rr'):
                    score += 8 - i
                else:
                    score += i
    return score

def get_p_spots(board, player, w):
    score = 0
    if(player == 'Rr'):
        if(board[0][0] == None):
            score += w
        if(board[0][2] == None):
            score += w
        if(board[0][4] == None):
            score += w
        if(board[0][6] == None):
            score += w
    else:
        if(board[7][1] == None):
            score += w
        if(board[7][3] == None):
            score += w
        if(board[7][5] == None):
            score += w
        if(board[7][7] == None):
            score += w
    return score

def get_defenders(board, player, w):
    score = 0
    if(player == 'Rr'):
        for(j, value) in enumerate(board[7]):
            if(str(value) in player):
                score += w
        for(j, value) in enumerate(board[6]):
            if(str(value) in player):
                score += w
    else:
        for(j, value) in enumerate(board[0]):
            if(str(value) in player):
                score += w
        for(j, value) in enumerate(board[1]):
            if(str(value) in player):
                score += w
    return score
def get_winner(board, player):
    enemy = ("Rr" if (player == "Bb") else "Bb")
    for (i, row) in enumerate(board):
        for (j, value) in enumerate(row):
            if(str(value) not in player):
                continue
            if(len(get_valid_moves(board, player, i, j)) != 0):
                return None
    return enemy

def play_game(brain1, brain2):
    board = "b,null,b,null,b,null,b,null"
    board += ",null,b,null,b,null,b,null,b"
    board += ",b,null,b,null,b,null,b,null"
    board += ",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null"
    board += ",null,r,null,r,null,r,null,r"
    board += ",r,null,r,null,r,null,r,null"
    board += ",null,r,null,r,null,r,null,r"
    board = board.split(',')

    #change 1d array to 2d array
    board = [board[:8],board[8:16],board[16:24],board[24:32],board[32:40],board[40:48],board[48:56],board[56:64]]

    player = "Rr"
    enemy = "Bb"
    winner = None
    turn_number = 0
    #change all instances of "null" string to None
    for (i, row) in enumerate(board):
        for (j, value) in enumerate(row):
            if(value == "null"):
                board[i][j] = None;
    while(winner == None):
        turn_number += 1
        root = Node(board, player)
        fill_tree(root, 3)
        if(player == "Rr"):
            score = mini_max(root, brain1, True, float('-inf'), float('inf'))
        else:
            score = mini_max(root, brain2, True, float('-inf'), float('inf'))
        move = None
        for child in root.children:
            if( child.score == score ):
                move = child.move
                break
        #print("move: ",move)
        try:
            board = execute_move(board, move, player)
        except TypeError:
            print("there was a type error")
            print("board:")
            for row in board:
                print(row)
            print("move: ",move)
            print("player: ",player)
            print("score: ",score)
            for child in root.children:
                print("child move: ", child.move)
                print("child score: ", child.score)
            sys.exit()
        player, enemy = enemy, player
        winner = get_winner(board, player)
        if(turn_number > 100):
            winner = "draw"
        #print("current board:")
        #for row in board:
            #print(row)
    return winner

def mutate_winners(player, pop_size, winners):
    new_players = []
    for x in range(pop_size):
        cross = random.randint(1,len(winners[0].weights)-1)
        parent_a = random.choice(winners)
        parent_b = random.choice(winners)
        new_weights = parent_a.weights[:cross]
        new_weights.extend(parent_b.weights[cross:])
        for weight in new_weights:
            weight += round(random.uniform(-.3,.3),2)
        new_players.append(Brain(player, new_weights))
    return new_players

#parse arguments, and start script
if __name__ == '__main__':
    #check the number of arguements is correct
    if(len(sys.argv) != 3):
        usage()
        exit(1)
    board = sys.argv[1].replace("\"","").split(",")
    #change 1d array to 2d array
    board = [board[:8],board[8:16],board[16:24],board[24:32],board[32:40],board[40:48],board[48:56],board[56:64]]

    player = sys.argv[2]

    #change all instances of "null" string to None
    for (i, row) in enumerate(board):
        for (j, value) in enumerate(row):
            if(value == "null"):
                board[i][j] = None;
    
    root = Node(board, player)
    fill_tree(root, 5)
    brain = Brain(player, [0.61, 3.03, 1.95, 3.9, 1.17, 3.88, 1.54, 0.64, 2.16]) 
    score = mini_max(root, brain, True, float('-inf'), float('inf'))
    move = None
    for child in root.children:
        if( child.score == score ):
            print(child.move)
            move = child
            break
    #for row in move.board:
        #print(row)



