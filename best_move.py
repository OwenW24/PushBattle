from PushBattle import Game, PLAYER1, PLAYER2

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
                        scoreOfMove = self.minimax_placement(game, i, j, 5, float('-inf'), float('inf'))
                        if (scoreOfMove > bestScore):
                            bestScore = scoreOfMove
                            bestRow = i
                            bestCol = j
            move = [bestRow, bestCol]
            print(move)
        else:
            bestMoveRow = 0
            bestMoveCol = 0
            for i in range(8):
                for j in range(8):
                    if board[i][j] == player:
                        for x in range(8):
                            for y in range(8):
                                if game.is_valid_move(i, j, x, y):
                                    scoreOfMove = self.minimax_movement(game, i, j, x, y, 5, float('-inf'), float('inf'))
                                    if (scoreOfMove > bestScore):
                                        bestScore = scoreOfMove
                                        bestRow = i
                                        bestCol = j
                                        bestMoveRow = x
                                        bestMoveCol = y
            move = [bestRow, bestCol, bestMoveRow, bestMoveCol]
            print(move)
        return move

    # call w/ minimax_placement([game], [row], [col], 5, float('inf'), float(inf))
    def minimax_placement(self, game, row, col, depth, alpha, beta):
        if depth == 0:
            return 0
        
        newGame = game
        newGame.place_checker(row, col)

        if newGame.check_winner() == PLAYER1:
            return 1
        elif newGame.check_winner() == PLAYER2:
            return -1

        max_eval = float('-inf')
        for i in range(8):
            for j in range(8):
                if newGame.is_valid_placement(i, j):
                    eval_score = self.minimax_placement(newGame, i, j, depth - 1, alpha, beta)
                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
        return max_eval

    # call w/ minimax_placement([game], [init_row], [init_col], [init_nrow], [init_ncol], 5, float('inf'), float(inf))
    def minimax_movement(self, game, init_row, init_icol, new_row, new_col, depth, alpha, beta):
        if depth == 0:
            return 0
        
        newGame = game
        newGame.move_checker(init_row, init_icol, new_row, new_col)

        if newGame.check_winner() == PLAYER1:
            return 1
        elif newGame.check_winner() == PLAYER2:
            return -1

        max_eval = float('-inf')
        for i in range(8):
            for j in range(8):
                if newGame.is_valid_move(new_row, new_col, i, j):
                    eval_score = self.minimax_placement(newGame, new_row, new_col, i, j, depth - 1, alpha, beta)
                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
        return max_eval