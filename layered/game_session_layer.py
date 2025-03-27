import math
import numpy as np
from enum import Enum
from game_layer import GameLayer, Board


# Player Management Layer constants
PLAYER_1 = 1
PLAYER_2 = 2  # represents another player or the AI


class GameMode(Enum):
    SINGLE_PLAYER = 1,
    MULTI_PLAYER = 2,


class MoveResult:
    def __init__(self,
                 winner: int | None,
                 is_draw: bool,
                 is_over: bool,
                 game_mode: GameMode,
                 moves: list[tuple[int, int, int]]):
        self.winner = winner
        self.is_draw = is_draw
        self.is_over = is_over
        self.game_mode = game_mode
        self.moves = moves


class GameSessionLayer:
    def __init__(self):
        self._current_player = PLAYER_1
        self._game_mode = None  # set when game is started
        self._game = GameLayer()

    def start_game(self, game_mode: GameMode) -> Board:
        self._game_mode = game_mode
        return self._game.reset_board()

    def end_game(self) -> Board:
        self._game_mode = None
        return self._game.reset_board()

    def restart_game(self) -> Board:
        self._current_player = PLAYER_1
        return self._game.reset_board()

    def move(self, x: int) -> MoveResult:
        moves = []

        if not self._game.is_over:
            # make move on behalf of current player
            y = self._game.move(self._current_player, x)
            moves.append((x, y, self._current_player))

            if self._game_mode == GameMode.SINGLE_PLAYER:  # make move on behalf of AI
                x2 = self._get_ai_move()
                y2 = self._game.move(PLAYER_2, x2)
                moves.append((x2, y2, PLAYER_2))
            else:  # switch player
                self._current_player = PLAYER_2 if self._current_player == PLAYER_1 else PLAYER_1

        return MoveResult(game_mode=self._game_mode,
                          winner=self._game.winner,
                          is_draw=self._game.is_draw,
                          is_over=self._game.is_over,
                          moves=moves)

    ####################
    # Modified from my project submission for Dr. Hahsler's AI course
    #       Utilizes UCB1 to find best available available move in 1000 playoffs
    #       Utility function treats ties as losses
    ####################
    def _get_ai_move(self) -> int:
        root = {"u": 0, "n": 0}
        leafs = {move: {"u": 0, "n": 0} for move in self._game.open_moves}

        for _ in range(1000):
            move = None
            for l_move in leafs:
                if move is None:
                    move = l_move
                elif self._ucb1(leafs[l_move], root["n"]) > self._ucb1(leafs[move], root["n"]):
                    move = l_move

            playout_utility = self._simulate(self._current_player, move)

            # 4. back propagation
            leafs[move]["u"] += playout_utility
            leafs[move]["n"] += 1
            root["n"] += 1

        return self._choose_best_action(leafs)

    def _ucb1(self, leaf, parent_n):
        if leaf["n"] == 0:
            return +math.inf

        C = math.sqrt(2)
        avg_utility_per_playout = leaf["u"] / leaf["n"]
        playout_quotient = math.sqrt(math.log(parent_n) / leaf["n"])

        return avg_utility_per_playout + C * playout_quotient

    def _simulate(self, player: int, x: int):
        p_game = self._game.result(player, x)
        while True:
            if p_game.is_over:
                return 1 if p_game.winner == player else -1

            # alternate random moves until terminal state is reached
            all_actions = p_game.open_moves
            choice = np.random.randint(len(all_actions))
            next_action = all_actions[choice]

            p_game = p_game.result(PLAYER_2 if player == PLAYER_1 else PLAYER_1, next_action)

    def _choose_best_action(self, leafs):
        # choose leaf w/ most playouts
        best_action = None
        for l_action in leafs:
            if best_action is None:
                best_action = l_action
            elif leafs[l_action]["n"] > leafs[best_action]["n"]:
                best_action = l_action

        return best_action
