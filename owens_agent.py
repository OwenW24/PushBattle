import random
import copy
from PushBattle import Game, PLAYER1, PLAYER2, EMPTY, BOARD_SIZE, NUM_PIECES, _torus

'''
This is a sample implementation of an agent that just plays a random valid move every turn.
I would not recommend using this lol, but you are welcome to use functions and the structure of this.
'''

class OwensAgent:
    def __init__(self, player=PLAYER1):
        self.player = player
    
    # given the game state, gets all of the possible moves
    def get_possible_moves(self, game):
        """Returns list of all possible moves in current state."""
        moves = []
        current_pieces = game.p1_pieces if game.current_player == PLAYER1 else game.p2_pieces
        
        if current_pieces < NUM_PIECES:
            # placement moves
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    if game.board[r][c] == EMPTY:
                        moves.append((r, c))
        else:
            # movement moves
            for r0 in range(BOARD_SIZE):
                for c0 in range(BOARD_SIZE):
                    if game.board[r0][c0] == game.current_player:
                        for r1 in range(BOARD_SIZE):
                            for c1 in range(BOARD_SIZE):
                                if game.board[r1][c1] == EMPTY:
                                    moves.append((r0, c0, r1, c1))
        return moves
    
    def simulate_move(self, game, move):
        """Simulates a move and returns the new game state"""
        game_copy = copy.deepcopy(game)
        current_pieces = game_copy.p1_pieces if game_copy.current_player == PLAYER1 else game_copy.p2_pieces
        
        if current_pieces < NUM_PIECES:
            if game_copy.is_valid_placement(move[0], move[1]):
                game_copy.place_checker(move[0], move[1])
        else:
            if game_copy.is_valid_move(move[0], move[1], move[2], move[3]):
                game_copy.move_checker(move[0], move[1], move[2], move[3])
                
        return game_copy

    def count_aligned_pieces(self, game, player):
        """Counts the number of pieces that are aligned (2 in a row)"""
        count = 0
        dirs = [(0,1), (1,0), (1,1), (1,-1)]  # horizontal, vertical, diagonal
        
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if game.board[r][c] == player:
                    for dr, dc in dirs:
                        r2, c2 = _torus(r + dr, c + dc)
                        if game.board[r2][c2] == player:
                            count += 1
        return count

    def evaluate_position(self, game):
        """Evaluates the current game position"""
        # Check for win first
        winner = game.check_winner()
        if winner == self.player:
            return 1000
        elif winner == -self.player:
            return -1000
            
        # Count aligned pieces
        my_aligned = self.count_aligned_pieces(game, self.player)
        opp_aligned = self.count_aligned_pieces(game, -self.player)
        
        return my_aligned - opp_aligned

    def get_best_move(self, game):
        """Returns the best move using position evaluation"""
        possible_moves = self.get_possible_moves(game)
        if not possible_moves:
            return "forfeit"
            
        best_score = float('-inf')
        best_moves = []
        
        for move in possible_moves:
            # Simulate the move
            new_game = self.simulate_move(game, move)
            if new_game.check_winner() == self.player:
                return move  # Winning move found
                
            # Evaluate position after move
            score = self.evaluate_position(new_game)
            
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
        
        # Return the best move or a random choice among equally good moves
        return random.choice(best_moves)