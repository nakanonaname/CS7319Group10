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
    """Data transfer object that encapsulates data sent to UI from Game layer"""
    def __init__(self,
                 winner: int | None,
                 is_draw: bool,
                 is_over: bool,
                 moves: list[tuple[int, int, int]]):
        self.winner = winner
        self.is_draw = is_draw
        self.is_over = is_over
        self.moves = moves


class GameSessionLayer:
    """Manages player turn and encapsulates AI implementation"""

    def __init__(self):
        self._game_layer = GameLayer()
        self._current_player = None
        self._game_mode = None  # set when game starts

    @property
    def game_mode(self) -> GameMode | None:
        """Sets selected game mode, if game has started"""
        return self._game_mode

    @property
    def is_multiplayer(self) -> bool:
        """Returns whether the game mode is Multiplayer"""
        return self._game_mode == GameMode.MULTI_PLAYER

    @property
    def current_player(self) -> int:
        """Returns current player (PLAYER_1 or PLAYER_2)"""
        return self._current_player

    def start_session(self, game_mode: GameMode):
        """Starts a new game session"""
        self._game_mode = game_mode
        self.restart_session()

    def restart_session(self):
        """Restarts an existing game session"""
        self._current_player = PLAYER_1
        self._game_layer.reset()

    def move(self, x: int) -> MoveResult:
        """Returns the result of a performed move"""

        if self._game_layer.is_over:
            return self._create_move_result(moves=[])

        moves = []

        # make move on behalf of current player
        y = self._game_layer.move(self._current_player, x)
        moves.append((x, y, self._current_player))

        # switch players
        self._current_player = other(self._current_player)

        if not self._game_layer.is_over and self._game_mode == GameMode.SINGLE_PLAYER:  # get monte carlo move
            x2 = monte_carlo_move(self._game_layer, self._current_player)
            y2 = self._game_layer.move(self._current_player, x2)
            moves.append((x2, y2, self._current_player))

            # switch back to previous player
            self._current_player = other(self._current_player)

        return self._create_move_result(moves)

    def _create_move_result(self, moves: list[tuple[int, int, int]]) -> MoveResult:
        """Creates result from a move performed"""
        return MoveResult(winner=self._game_layer.winner,
                          is_draw=self._game_layer.is_draw,
                          is_over=self._game_layer.is_over,
                          moves=moves)


def other(player):
    """Return the other player"""
    return PLAYER_2 if player == PLAYER_1 else PLAYER_1


def monte_carlo_move(game_layer: GameLayer, player: int) -> int:
    """Uses Monte Carlo AI to get the best possible column"""
    root = {"u": 0, "n": 0}
    leafs = {move: {"u": 0, "n": 0} for move in game_layer.open_moves}

    for _ in range(2000):
        move = None
        for l_move in leafs:
            if move is None:
                move = l_move
            elif ucb1(leafs[l_move], root["n"]) > ucb1(leafs[move], root["n"]):
                move = l_move

        playout_utility = simulate(game_layer, player, move)

        # 4. back propagation
        leafs[move]["u"] += playout_utility
        leafs[move]["n"] += 1
        root["n"] += 1

    return choose_best_action(leafs)


def ucb1(leaf, parent_n):
    if leaf["n"] == 0:
        return +math.inf

    C = math.sqrt(2)
    avg_utility_per_playout = leaf["u"] / leaf["n"]
    playout_quotient = math.sqrt(math.log(parent_n) / leaf["n"])

    return avg_utility_per_playout + C * playout_quotient


def simulate(game_layer: GameLayer, player: int, x: int):
    the_player = player
    p_game = game_layer.simulate_move(the_player, x)

    while True:
        if p_game.is_over:
            return 1 if p_game.winner == player else -1

        # alternate random moves until terminal state is reached
        all_actions = p_game.open_moves
        choice = np.random.randint(len(all_actions))
        next_action = all_actions[choice]

        the_player = other(the_player)
        p_game = p_game.simulate_move(the_player, next_action)


def choose_best_action(leafs):
    # choose leaf w/ most playouts
    best_action = None
    for l_action in leafs:
        if best_action is None:
            best_action = l_action
        elif leafs[l_action]["n"] > leafs[best_action]["n"]:
            best_action = l_action

    return best_action
