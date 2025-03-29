import numpy as np


UNOCCUPIED = 0


class Board:
    """The internal board state used exclusively by Game Layer"""
    def __init__(self, grid):
        self._grid = grid
        self._width = len(self._grid[0])
        self._height = len(self._grid)

    @property
    def grid(self):
        return self._grid

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    def apply_move(self, player: int, x: int, y: int):
        self._grid[y, x] = player

    def copy(self):
        return Board(np.copy(self._grid))


class GameLayer:
    """Maintains board state and validates moves against game rules"""

    def __init__(self):
        self._board = self._create_board()
        self._winner = None

    def reset(self):
        """Reset game state"""
        self._board = self._create_board()
        self._winner = None

    @property
    def winner(self) -> int | None:
        """Returns winning player # if exists"""
        return self._winner

    @property
    def is_draw(self) -> bool:
        """Returns whether the game ended in a draw"""
        all_occupied = np.count_nonzero(self._board.grid == UNOCCUPIED) == 0
        return self._winner is None and all_occupied

    @property
    def is_over(self) -> bool:
        """Returns whether the game is over (draw or winner)"""
        return self._winner is not None or self.is_draw

    @property
    def open_moves(self) -> list[int]:
        """Returns list of playable columns (for use by AI agent)"""
        return [x for x in range(self._board.width)
                if np.count_nonzero(self._board.grid[:, x] == UNOCCUPIED) > 0]

    def move(self, player: int, x: int) -> int:
        """Validates the move, updates state, and checks for winner
            Returns the row in which the move was applied"""

        if self.is_over:
            raise Exception("Game is over")

        # determine if col is full
        if np.count_nonzero(self._board.grid[:, x] == UNOCCUPIED) == 0:
            raise Exception("Illegal move")

        # apply move in first available row within column
        y = np.where(self._board.grid[:, x] == UNOCCUPIED)[0][-1]
        self._board.apply_move(player, x, y)

        rows = [
            # horizontal (+/- 4 from played cell)
            [self._board.grid[y, x]
             for x in range(max(0, x - 4), min(x + 4, self._board.width))],

            # vertical (+/- 4 from played cell)
            [self._board.grid[y, x]
             for y in range(max(0, y - 4), min(y + 4, self._board.height))],

            # left -> right (up) diag (+/- 4 from played cell)
            [self._board.grid[y + n, x + n]
             for n in range(-4, 5)
             if
             0 <= x + n < self._board.width and 0 <= y + n < self._board.height],

            # left -> right (down) diag (+/- 4 from played cell)
            [self._board.grid[y - n, x + n]
             for n in range(-4, 5)
             if
             0 <= x + n < self._board.width and 0 <= y - n < self._board.height]
        ]

        # check adjacent rows for a winner
        for row in rows:
            if self._winner is not None:
                break

            if len(row) < 4 or row[len(row) // 2] != player:
                continue  # player must occupy middle to win horizontally

            num_adjacent = 0
            for n in row:
                if n == player:
                    num_adjacent += 1
                else:
                    num_adjacent = 0

                if num_adjacent >= 4:
                    self._winner = player
                    break

        return y

    def simulate_move(self, player: int, x: int):
        """Simulates a move. Does not modify existing board state"""
        game_copy = GameLayer()
        game_copy._winner = self._winner
        game_copy._board = self._board.copy()

        if not game_copy.is_over:  # applies move if board has open moves
            game_copy.move(player, x)

        return game_copy

    @staticmethod
    def _create_board() -> Board:
        """Returns empty board"""
        return Board(np.full((6, 7), UNOCCUPIED, dtype=int))
