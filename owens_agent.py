import random
import copy
import numpy as np
from collections import defaultdict
from PushBattle import Game, PLAYER1, PLAYER2, EMPTY, BOARD_SIZE, NUM_PIECES, _torus

class OwensAgent:
    def __init__(self, player=PLAYER1):
        self.player = player
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.1  # Exploration rate
        self.q_table = defaultdict(lambda: defaultdict(float))
        # Critical defensive positions when playing second
        self.defensive_positions = [
            (3, 3),  # Center defense
            (4, 4),  # Center defense
            (2, 2),  # Counter corners
            (2, 5),  # Counter middle
            (5, 2),  # Support position
            (5, 5)   # Support position
        ]

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
        self.player = game_copy.current_player  # Update player perspective based on current game state
        current_pieces = game_copy.p1_pieces if game_copy.current_player == PLAYER1 else game_copy.p2_pieces
        
        if current_pieces < NUM_PIECES:
            if game_copy.is_valid_placement(move[0], move[1]):
                game_copy.place_checker(move[0], move[1])
        else:
            if game_copy.is_valid_move(move[0], move[1], move[2], move[3]):
                game_copy.move_checker(move[0], move[1], move[2], move[3])
                
        return game_copy

    def get_state_key(self, game):
        """Convert board state to a string key for Q-learning"""
        # Include critical patterns in state representation
        state = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if game.board[r][c] != EMPTY:
                    state.append(f"{r},{c},{game.board[r][c]}")
        return "|".join(sorted(state))

    def get_pattern_score(self, game):
        """Evaluate dangerous patterns in the current state"""
        score = 0
        opponent = -self.player
        
        # Check for opponent's two-in-a-row patterns
        dirs = [(0,1), (1,0), (1,1), (1,-1)]
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if game.board[r][c] == opponent:
                    for dr, dc in dirs:
                        r2, c2 = _torus(r + dr, c + dc)
                        if game.board[r2][c2] == opponent:
                            score -= 50  # Heavily penalize opponent alignments
                            r3, c3 = _torus(r2 + dr, c2 + dc)
                            if game.board[r3][c3] == EMPTY:
                                score -= 25  # Extra penalty for potential wins
        return score

    def get_best_move(self, game):
        """Q-learning based move selection with pattern recognition"""
        self.player = game.current_player
        state = self.get_state_key(game)
        possible_moves = self.get_possible_moves(game)
        
        if not possible_moves:
            return "forfeit"

        # Early game defensive strategy when playing second
        if game.p1_pieces < 3 and self.player == PLAYER2:
            # Find opponent's pieces
            opponent_pieces = [(r,c) for r in range(BOARD_SIZE) 
                             for c in range(BOARD_SIZE) 
                             if game.board[r][c] == -self.player]
            
            # If opponent has aligned pieces, block immediately
            if len(opponent_pieces) >= 2:
                for pos in self.defensive_positions:
                    if game.board[pos[0]][pos[1]] == EMPTY:
                        test_game = self.simulate_move(game, pos)
                        if test_game.check_winner() != -self.player:
                            return pos

        # Exploitation vs Exploration
        if random.random() > self.epsilon:
            # Choose best move based on Q-values and pattern recognition
            best_move = None
            best_value = float('-inf')
            
            for move in possible_moves:
                # Simulate move
                new_game = self.simulate_move(game, move)
                if new_game.check_winner() == self.player:
                    return move
                
                # Combine Q-value with pattern recognition
                move_str = str(move)
                q_value = self.q_table[state][move_str]
                pattern_score = self.get_pattern_score(new_game)
                total_value = q_value + pattern_score
                
                if total_value > best_value:
                    best_value = total_value
                    best_move = move
            
            if best_move:
                return best_move

        # Random move if exploring or no Q-values available
        move = random.choice(possible_moves)
        
        # Update Q-table after move
        new_game = self.simulate_move(game, move)
        new_state = self.get_state_key(new_game)
        reward = 100 if new_game.check_winner() == self.player else self.get_pattern_score(new_game)
        
        # Q-learning update
        old_value = self.q_table[state][str(move)]
        next_max = max([self.q_table[new_state][str(m)] for m in self.get_possible_moves(new_game)], default=0)
        new_value = (1 - self.learning_rate) * old_value + self.learning_rate * (reward + self.discount_factor * next_max)
        self.q_table[state][str(move)] = new_value
        
        return move

    def count_aligned_pieces(self, game, player):
        """Simplified alignment check focusing on winning patterns"""
        count = 0
        dirs = [(0,1), (1,0), (1,1), (1,-1)]
        
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if game.board[r][c] == player:
                    for dr, dc in dirs:
                        r2, c2 = _torus(r + dr, c + dc)
                        if game.board[r2][c2] == player:
                            # Double weight for two aligned pieces
                            count += 2
                            # Check for potential win
                            r3, c3 = _torus(r2 + dr, c2 + dc)
                            if game.board[r3][c3] == EMPTY:
                                count += 3  # Extra points for potential winning move
        return count

    def minimax(self, game, depth, alpha, beta, maximizing_player):
        """Minimax algorithm with alpha-beta pruning"""
        if depth == 0 or game.check_winner() != EMPTY:
            return self.evaluate_position(game), None
            
        possible_moves = self.get_possible_moves(game)
        if not possible_moves:
            return -1000 if maximizing_player else 1000, None
            
        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for move in possible_moves:
                new_game = self.simulate_move(game, move)
                eval_score, _ = self.minimax(new_game, depth - 1, alpha, beta, False)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in possible_moves:
                new_game = self.simulate_move(game, move)
                eval_score, _ = self.minimax(new_game, depth - 1, alpha, beta, True)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def evaluate_position(self, game):
        """Position evaluation specifically countering best_move2 strategy"""
        current_player = game.current_player
        opponent = PLAYER2 if current_player == PLAYER1 else PLAYER1
        
        score = 0
        
        # Immediate outcomes
        winner = game.check_winner()
        if winner == current_player:
            return 1000
        elif winner == opponent:
            return -1000
            
        # Counter best_move2's common patterns
        score += self.evaluate_pattern_control(game, current_player, opponent)
        
        # Analyze piece formations
        score += self.evaluate_formations(game, current_player) * 2
        score -= self.evaluate_formations(game, opponent) * 3  # Higher weight on opponent threats
        
        return score

    def evaluate_pattern_control(self, game, current_player, opponent):
        """Evaluate board control specifically against best_move2 patterns"""
        score = 0
        
        # Reward control of key positions
        key_positions = [(3,3), (3,4), (4,3), (4,4), (2,3), (2,4)]
        for r, c in key_positions:
            if game.board[r][c] == current_player:
                score += 15
            elif game.board[r][c] == opponent:
                score -= 20
                
        # Penalize opponent's corner control (common best_move2 strategy)
        corners = [(0,0), (0,7), (7,0), (7,7)]
        for r, c in corners:
            if game.board[r][c] == opponent:
                score -= 25
                
        # Extra points for defensive formations
        if self.has_defensive_formation(game, current_player):
            score += 30
            
        return score

    def has_defensive_formation(self, game, player):
        """Check for specific defensive formations"""
        formations = [
            [(3,3), (3,4), (4,3)],  # Triangle formation
            [(4,4), (4,3), (3,4)],  # Inverse triangle
            [(3,3), (4,4), (3,4)]   # Diagonal support
        ]
        
        for formation in formations:
            if all(game.board[r][c] == player for r, c in formation):
                return True
        return False

    def breaks_opponent_formation(self, game, move, opponent):
        """Check if move breaks opponent's connected pieces"""
        test_game = self.simulate_move(game, move)
        
        # Count opponent's connected pieces before and after move
        before_count = sum(self.count_adjacent_pieces(game, r, c, opponent) 
                         for r in range(BOARD_SIZE) 
                         for c in range(BOARD_SIZE) 
                         if game.board[r][c] == opponent)
        
        after_count = sum(self.count_adjacent_pieces(test_game, r, c, opponent) 
                         for r in range(BOARD_SIZE) 
                         for c in range(BOARD_SIZE) 
                         if test_game.board[r][c] == opponent)
                         
        return after_count < before_count

    def blocks_winning_move(self, game, opponent):
        """Check if move blocks opponent's potential win"""
        dirs = [(0,1), (1,0), (1,1), (1,-1)]
        
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if game.board[r][c] == opponent:
                    for dr, dc in dirs:
                        r2, c2 = _torus(r + dr, c + dc)
                        if game.board[r2][c2] == opponent:
                            r3, c3 = _torus(r2 + dr, c2 + dc)
                            if game.board[r3][c3] == self.player:
                                return True
        return False