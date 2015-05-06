import genetic_programming as gp
from random import random, randint, choice
# using genetic programming to play a tic_tac_toe game

def tic_tac_toe(player1, player2):
    # board view for player1
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # board view for player2
    # board2 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    def eval_board():

        winning = (board[0] == board[1] == board[2] == 1) or (board[3] == board[4] == board[5] == 1) or (
            board[6] == board[7] == board[8] == 1)
        
        winning = winning or (board[0] == board[3] == board[6] == 1) or (
            board[1] == board[4] == board[7] == 1) or (board[2] == board[5] == board[8] == 1)
        
        winning = winning or (board[0] == board[4] == board[8] == 1) or (
            board[2] == board[4] == board[6] == 1) 
        
        return winning
        
        
    
    # take turns to play the game
    for i in range(9):
        # print board
        # player1's turn
        if i % 2 == 0:
            board = [-x for x in board]
            # make move - return an index to place 1
            indx = player1.evaluate(board) % 8
            if board[indx] != 0:
                return 'player2'
            
            board[indx] = 1            
            
            if eval_board():
                return 'player1'
            
        # player2's turn
        else:
            board = [-x for x in board]
            # make move
            indx = player2.evaluate(board) % 8
            if board[indx] != 0:
                return 'player1'
            
            board[indx] = 1               
            
            if eval_board():
                return 'player2'            
        
    return 'tie'
    
    
#p1 = gp.make_random_tree(9, gp.flist)
#p2 = gp.make_random_tree(9, gp.flist)
#p1.display()
#p2.display()
#print tic_tac_toe(p1, p2)   
    
def ttc_tournament(players):
    # count losses
    losses = [0 for p in players]
    
    # Every player plays against every other player
    for i in range(len(players)):
        for j in range(len(players)):
            if i == j: 
                continue
            
            # result of the game
            result = tic_tac_toe(players[i], players[j])
            
            if result == 'player1':
                losses[j] += 3
            elif result == 'player2':
                losses[i] += 3
            elif result == 'tie':
                losses[i] += 1
                losses[j] += 1
                
    z = zip(losses, players)
    z.sort()
    return z


class human_player:
    def evaluate(self, board):
        # display the board
        for i in range(len(board)):
            if i % 3 == 0:
                print 
            if board[i] == 0:
                print ".",
            elif board[i] == 1:
                # human player sees O alwyas
                print "O",
            else:
                print "X",
            
        print 
        print "Enter Move:"
        move = int(raw_input())
        return move
            
        
        


winner = gp.evolve(9, 100, gp.flist, ttc_tournament, max_gen = 100)
winner.display()
        
        
tic_tac_toe(winner, human_player())
        