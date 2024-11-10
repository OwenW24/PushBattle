# Push Battle

    This is a project created for the 2024 Datathon "Push Battle" Challenge.
    The following "Rules" and "Board" and "Restrictions" sections were provided by the TAMU Datathon Team.

# The Rules

    Push Battle is a two player game played on an 8x8 grid
    Each player will have eight pieces where players take turn placing pieces on the board
    When a piece is placed on the board, all pieces adjacent to the placed piece are pushed away, unless there is another piece behind it preventing it from being pushed
    If a piece gets pushed off the side of the board it will appear directly on the other side of the board
    If all eight pieces are on the board, the player must pick up one of the pieces and move it to any other spot on the board
    Players win when three of their pieces are in a row

# The Board
    The board will be represented by an 8x8 2D array. In the placement stage of the game, the player places a piece on the board at [r, c]. Once all checkers have been placed, the player will make a move [r0, c0, r1, c1] which moves one of their existing pieces at (r0, c0) to (r1, c1).
    For readability purposes,the moves will be displayed on the visualizer in algebraic notation.

# Restrictions
    - Agents will be given 5 seconds to make a move. If the time limit is exceeded, agents will be given another 5 seconds to make a fallback move. If the time limit is exceeded again, a random move will be made for the agent. If this occurs 5 times, the agent will forfeit.
    - If your agent makes an invalid move (i.e. placing a piece out of bounds or on an existing piece, attempting to move an opponent's piece, etc.), it will immediately forfeit (lose) the game
    - No network access
    - 1 CPU Core
    - 1 GB RAM
    - 1 GB VRAM

# Our Approach (basically)
    The primary approach taken for this program was implementation of a minimax algorithm to predict and select
    future moves. Initially we included Alpha-Beta Pruning to speed up our algorithm, but later decided for our
    purposes we found it to be unneccessary. 
    