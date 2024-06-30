import chess

from ..evaluators import Evaluator

from .abstract import Searcher, SearchResult


class AlphaBetaSearcher(Searcher):
    """Searcher based on Alpha-Beta Pruning"""

    def __init__(self, evaluator: Evaluator, depth: int):
        assert depth >= 0

        self.evaluator: Evaluator = evaluator
        self.depth: int = depth

        self.board: chess.Board | None = None
        self.move_count_at_search_begin: int | None = None

        self.alpha: float = 0.0
        self.beta: float = 0.0

    def get_search_move_stack(self) -> list[chess.Move]:
        """Get the list of moves the leads to the current node in the search"""
        return self.board.move_stack[self.move_count_at_search_begin:]

    def init_search(self, board: chess.Board) -> None:
        """Initialize internal variables of the `Searcher` for search begin"""
        self.board = board
        self.move_count_at_search_begin = len(board.move_stack)
        self.alpha = float("-inf")
        self.beta = float("inf")

    def search(self, board: chess.Board) -> SearchResult:
        self.init_search(board)
        search_result = self._alpha_beta(self.depth, self.alpha, self.beta)
        return search_result

    def _alpha_beta(self, depth: int, alpha: float, beta: float) -> SearchResult:
        anchor = self._check_recursion_anchors(depth)
        if anchor is not None:
            return anchor

        return self._recurse(depth, alpha, beta)

    def _check_recursion_anchors(self, depth: int) -> SearchResult | None:
        # if one of the conditions to break the Alpha-Beta recursion is met, return the final value

        if depth <= 0:
            return SearchResult.from_score(self.evaluator.eval(self.board), self.get_search_move_stack())

        if self.board.is_checkmate():
            return SearchResult.from_mate(chess.BLACK if self.board.turn == chess.WHITE else chess.WHITE,
                                          self.get_search_move_stack())

        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return SearchResult.from_draw(self.get_search_move_stack())

    def _recurse(self, depth: int, alpha: float, beta: float) -> SearchResult:
        maximize = self.board.turn == chess.WHITE
        best_result = SearchResult.from_mate(chess.BLACK if self.board.turn == chess.WHITE else chess.WHITE,
                                             self.get_search_move_stack())
        selector = max if maximize else min

        for move in self.board.legal_moves:
            self.board.push(move)
            best_result = selector(best_result, self._alpha_beta(depth - 1, alpha, beta))
            self.board.pop()

            if maximize:
                alpha = max(alpha, best_result.get_effective_score())
                if alpha >= beta:
                    break
            else:
                beta = min(beta, best_result.get_effective_score())
                if beta <= alpha:
                    break

        return best_result
