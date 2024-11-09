from PushBattle import Game, PLAYER1, PLAYER2, EMPTY
import numpy as np

class Minimax:

    def get_best_move(self, game, board, player):
        bestScore = float('-inf')
        bestRow = 0
        bestCol = 0
        isMovement = (PLAYER1 in board) or (PLAYER2 in board)
        if (not isMovement):
            for i in range(8):
                for j in range(8):
                    if game.is_valid_placement(i, j):
                        scoreOfMove = self.minimax_placement(game, i, j, 5, float('-inf'), float('inf'), player, player)
                        print("testing", i, j, ":", scoreOfMove)
                        if (scoreOfMove > bestScore):
                            bestScore = scoreOfMove
                            bestRow = i
                            bestCol = j
            move = [bestRow, bestCol]
            # print(move)
        else:
            bestMoveRow = 0
            bestMoveCol = 0
            for i in range(8):
                for j in range(8):
                    if board[i][j] == player:
                        for x in range(8):
                            for y in range(8):
                                if game.is_valid_move(i, j, x, y):
                                    scoreOfMove = self.minimax_movement(game, i, j, x, y, 5, float('-inf'), float('inf'), player, player)
                                    if (scoreOfMove > bestScore):
                                        bestScore = scoreOfMove
                                        bestRow = i
                                        bestCol = j
                                        bestMoveRow = x
                                        bestMoveCol = y
            move = [bestRow, bestCol, bestMoveRow, bestMoveCol]
            # print(move)
        return move

# call w/ minimax_placement([game], [row], [col], 5, float('inf'), float(inf))
    def minimax_placement(self, game, row, col, depth, alpha, beta, currPlayer, targetPlayer):
        if depth == 0:
            return 0
        
        newGame = game

        newGame.currentPlayer = currPlayer
        newGame.place_checker(row, col)

        winner = newGame.check_winner()
        if winner == targetPlayer:
            return 1
        elif winner != EMPTY:
            return -1
        
        if currPlayer == PLAYER1:
            currPlayer = PLAYER2
        else:
            currPlayer = PLAYER1

        totalScore = 0
        if currPlayer == targetPlayer:
            best_score = -float('inf') 
            for i in range(8):
                for j in range(8):
                    if newGame.is_valid_placement(i, j):
                        eval_score = self.minimax_placement(newGame, i, j, depth - 1, alpha, beta, currPlayer, targetPlayer)
                        totalScore += eval_score
                        best_score = max(best_score, totalScore)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
        else:
            best_score = float('inf')
            for i in range(8):
                for j in range(8):
                    if newGame.is_valid_placement(i, j):
                        eval_score = self.minimax_placement(newGame, i, j, depth - 1, alpha, beta, currPlayer, targetPlayer)
                        totalScore += eval_score
                        best_score = min(best_score, totalScore)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break

        return totalScore

    # call w/ minimax_placement([game], [init_row], [init_col], [init_nrow], [init_ncol], 5, float('inf'), float(inf))
    def minimax_movement(self, game, init_row, init_col, new_row, new_col, depth, alpha, beta, currPlayer, targetPlayer):
        if depth == 0:
            return 0
        
        newGame = game

        newGame.currentPlayer = currPlayer
        newGame.move_checker(init_row, init_col, new_row, new_col)

        winner = newGame.check_winner()
        if winner == targetPlayer:
            return 1
        elif winner != EMPTY:
            return -1
        
        if currPlayer == PLAYER1:
            currPlayer = PLAYER2
        else:
            currPlayer = PLAYER1

        if currPlayer == targetPlayer:
            best_score = -float('inf') 
            for i in range(8):
                for j in range(8):
                    if newGame.is_valid_move(new_row, new_col, i, j):
                        eval_score = self.minimax_placement(newGame, new_row, new_col, i, j, depth - 1, alpha, beta, currPlayer, targetPlayer)
                        best_score = max(best_score, eval_score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
        else:
            best_score = float('inf')
            for i in range(8):
                for j in range(8):
                    if newGame.is_valid_placement(i, j):
                        eval_score = self.minimax_placement(newGame, new_row, new_col, i, j, depth - 1, alpha, beta, currPlayer, targetPlayer)
                        best_score = min(best_score, eval_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break

        return best_score