import chess

from ..evaluators import Evaluator
from .abstract import Searcher


class MinimaxSearcher(Searcher):
    """Searcher based on the Minimax algorithm"""

    def __init__(self, evaluator: Evaluator, depth: int):
        assert depth >= 0

        self.evaluator = evaluator
        self.depth = depth

    def search(self, board: chess.Board) -> float:
        return self._minimax(board, self.depth)

    def _minimax(self, board: chess.Board, depth: int) -> float:
        # Apply Minimax to `board` with the given search `depth`

        anchor = self._check_recursion_anchors(board, depth)
        if anchor is not None:
            return anchor

        return self._recurse_minimax(board, depth)

    def _check_recursion_anchors(self, board: chess.Board, depth: int) -> float | None:
        # if one of the conditions to break the Minimax recursion is met, return the final value

        if depth <= 0:
            return self.evaluator.eval(board)

        if board.is_checkmate():
            return -10_000 if board.turn == chess.WHITE else 10_000

        if board.is_stalemate() or board.is_insufficient_material():
            return 0

    def _recurse_minimax(self, board: chess.Board, depth: int):
        # Continue the search at the next lower level

        best_value = float("-inf") if board.turn == chess.WHITE else float("inf")
        selector = max if board.turn == chess.WHITE else min

        for move in board.legal_moves:
            board.push(move)
            best_value = selector(best_value, self._minimax(board, depth - 1))
            board.pop()

        return best_value
