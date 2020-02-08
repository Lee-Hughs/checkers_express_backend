#!/usr/bin/python3.5
import sys

if(len(sys.argv) != 3 ):
    exit(1)
board = sys.argv[1]
player = sys.argv[2]
print("board: ",board)
print("player: ",player)
sys.stdout.flush()
