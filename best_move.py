from PushBattle import Game, PLAYER1, PLAYER2

# call w/ minimax_placement([game], [row], [col], 5, float('inf'), float(inf))
def minimax_placement(game, row, col, depth, alpha, beta):
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
                eval_score = minimax_placement(newGame, i, j, depth - 1, alpha, beta)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
    return max_eval

# call w/ minimax_placement([game], [init_row], [init_col], [init_nrow], [init_ncol], 5, float('inf'), float(inf))
def minimax_movement(game, init_row, init_icol, new_row, new_col, depth, alpha, beta):
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
            if newGame.is_valid_movement(new_row, new_col, i, j):
                eval_score = minimax_placement(newGame, new_row, new_col, i, j, depth - 1, alpha, beta)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
    return max_eval