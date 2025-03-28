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
        self._dims = (6, 7)
        self._board = Board(np.full(self._dims, UNOCCUPIED, dtype=int))
        self._winner = None
        self._is_draw = False

    def reset_board(self) -> Board:
        self._board = Board(np.full(self._dims, UNOCCUPIED, dtype=int))
        self._winner = None
        self._is_draw = False
        return self._board

    @property
    def winner(self):
        return self._winner

    @property
    def is_draw(self):
        return self._winner is None and np.count_nonzero(self._board.grid == 0) == UNOCCUPIED

    @property
    def is_over(self):
        return self._is_draw or self._winner is not None

    def move(self, player: int, x: int) -> int:
        if self.is_over:
            raise Exception("Game is over")

        # determine if col is full
        if np.count_nonzero(self._board.grid[:, x] == UNOCCUPIED) == 0:
            raise Exception("Illegal move")

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

        # check for winner
        for row in rows:
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

            if self._winner is not None:
                break

        return y

    @property
    def open_moves(self):
        return [x for x in range(self._board.width)
                if np.count_nonzero(self._board.grid[:, x] == UNOCCUPIED) > 0]

    def simulate_move(self, player: int, x: int):
        """Simulates a move. Does not modify existing board state"""
        game_copy = GameLayer()
        game_copy._board = self._board.copy()
        game_copy._winner = self._winner
        game_copy._is_draw = self._is_draw

        if not game_copy.is_over:
            game_copy.move(player, x)

        return game_copy
