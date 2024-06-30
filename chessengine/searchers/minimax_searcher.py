import chess

from ..evaluators import Evaluator
from .abstract import Searcher, SearchResult


class MinimaxSearcher(Searcher):
    """Searcher based on the Minimax algorithm"""

    def __init__(self, evaluator: Evaluator, depth: int):
        assert depth >= 0

        self.evaluator = evaluator
        self.depth = depth

        self.board: chess.Board | None = None
        self.move_count_at_search_begin: int | None = None

    def get_search_move_stack(self) -> list[chess.Move]:
        """Get the list of moves the leads to the current node in the search"""
        return self.board.move_stack[self.move_count_at_search_begin:]

    def init_search(self, board: chess.Board) -> None:
        """Initialize internal variables of the `Searcher` for search begin"""
        self.board = board
        self.move_count_at_search_begin = len(board.move_stack)

    def search(self, board: chess.Board) -> SearchResult:
        self.init_search(board)
        search_result = self._minimax(self.depth)

        return search_result

    def _minimax(self, depth: int) -> SearchResult:
        anchor = self._check_recursion_anchors(depth)
        if anchor is not None:
            return anchor

        return self._recurse_minimax(depth)

    def _check_recursion_anchors(self, depth: int) -> SearchResult | None:
        # if one of the conditions to break the Minimax recursion is met, return the final value

        if depth <= 0:
            return SearchResult.from_score(self.evaluator.eval(self.board), self.get_search_move_stack())

        if self.board.is_checkmate():
            return SearchResult.from_mate(chess.BLACK if self.board.turn == chess.WHITE else chess.WHITE,
                                          self.get_search_move_stack())

        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return SearchResult.from_draw(self.get_search_move_stack())

    def _recurse_minimax(self, depth: int):
        best_result = SearchResult.from_mate(chess.BLACK if self.board.turn == chess.WHITE else chess.WHITE,
                                             self.get_search_move_stack())
        selector = max if self.board.turn == chess.WHITE else min

        for move in self.board.legal_moves:
            self.board.push(move)
            best_result = selector(best_result, self._minimax(depth - 1))
            self.board.pop()

        return best_result
