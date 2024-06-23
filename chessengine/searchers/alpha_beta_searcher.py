import chess

from ..evaluators import Evaluator

from .abstract import Searcher


class AlphaBetaSearcher(Searcher):
    """Searcher based on Alpha-Beta Pruning"""

    def __init__(self, evaluator: Evaluator, depth: int):
        assert depth >= 0

        self.evaluator = evaluator
        self.depth = depth

        self.board = None
        self.alpha = 0.0
        self.beta = 0.0

    def search(self, board: chess.Board) -> float:
        self.board = board
        self.alpha = float("-inf")
        self.beta = float("inf")

        search_result = self._alpha_beta(self.depth, self.alpha, self.beta)

        self.board = None
        return search_result

    def _alpha_beta(self, depth: int, alpha: float, beta: float) -> float:
        anchor = self._check_recursion_anchors(depth)
        if anchor is not None:
            return anchor

        return self._recurse(depth, alpha, beta)

    def _check_recursion_anchors(self, depth: int) -> float | None:
        # if one of the conditions to break the Alpha-Beta recursion is met, return the final value

        if depth <= 0:
            return self.evaluator.eval(self.board)

        if self.board.is_checkmate():
            return -10_000 if self.board.turn == chess.WHITE else 10_000

        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return 0

    def _recurse(self, depth: int, alpha: float, beta: float):
        maximize = self.board.turn == chess.WHITE
        best_value = float("-inf") if maximize else float("inf")
        selector = max if maximize else min

        for move in self.board.legal_moves:
            self.board.push(move)
            best_value = selector(best_value, self._alpha_beta(depth - 1, alpha, beta))
            self.board.pop()

            if maximize:
                alpha = max(alpha, best_value)
                if alpha >= beta:
                    break
            else:
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

        return best_value
