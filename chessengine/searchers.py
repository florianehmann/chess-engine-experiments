"""Move tree searching functions"""

from abc import ABC, abstractmethod
from enum import Enum, auto

import chess

from .cache import ChessCache
from .evaluators import Evaluator


class SearchResultType(Enum):
    """What type of result the searcher has found"""
    SCORE = auto()
    """The search returns a regular evaluation score."""
    MATE = auto()
    """The search determines that there is a guaranteed mate in a number of moves for the current color."""


# pylint: disable=attribute-defined-outside-init
class SearchResult:
    """Result of a search into the move tree.

    This class cannot be instantiated directly but is constructed in the factory methods :meth:`from_score` and
    :meth:`from_mate`, depending on the :class:`SearchResultType` of the result.
    """

    def __init__(self):
        raise TypeError("SearchResult cannot be instantiated directly, use factory methods")

    def __new__(cls):
        return super().__new__(cls)

    @classmethod
    def from_score(cls, score: float):
        """Create a search result that represents a regular evaluation score."""

        instance = cls.__new__(cls)
        instance.type = SearchResultType.SCORE
        instance.score = score

        return instance

    @classmethod
    def from_mate(cls, move_sequence: list[chess.Move]):
        """Create a search result that represents forced mate in a certain number of moves."""

        instance = cls.__new__(cls)
        instance.type = SearchResultType.MATE
        instance.move_sequence = move_sequence

        return instance


# pylint: disable=too-few-public-methods
class Searcher(ABC):
    """Search algorithm that provides an evaluation of a chess position based on searching in the tree of
    possible moves"""
    @abstractmethod
    def search(self, board: chess.Board) -> float:
        """Performs the tree search and returns an evaluation in centi pawns"""


class MinimaxSearcher(Searcher):
    """Searcher based on the Minimax algorithm"""

    def __init__(self, evaluator: Evaluator, depth: int):
        assert depth > 0

        self.evaluator = evaluator
        self.depth = depth

    def search(self, board: chess.Board) -> float:
        return minimax(board, self.evaluator, self.depth, board.turn == chess.WHITE)


# pylint: disable=too-few-public-methods
class AlphaBetaSearcher(Searcher):
    """Searcher based on Alpha-Beta Pruning"""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        evaluator: Evaluator,
        depth: int,
        alpha: float = -1_000_000,
        beta: float = +1_000_000,
        cachesize: int = 0,
    ):
        assert depth >= 0
        assert cachesize >= 0

        self.evaluator = evaluator
        self.depth = depth
        self.alpha = alpha
        self.beta = beta

        self.cache = None
        if cachesize > 0:
            self.cache = ChessCache(maxsize=cachesize)

    def search(self, board: chess.Board) -> float:
        result = None
        if self.cache is None:
            result = alpha_beta_search(
                board, self.evaluator, self.depth, self.alpha, self.beta
            )
        else:
            result = cached_alpha_beta_search(
                board, self.evaluator, self.cache, self.depth, self.alpha, self.beta
            )

        return result


def minimax(
    board: chess.Board, evaluator: Evaluator, depth: int, maximize: bool
) -> float:
    """Minimax algorithm for search-based evaluation of a chess position

    Parameters
    ----------
    board
        State of the chess board to be evaluated
    evaluator
        Evaluation function used at leaf nodes
    depth
        The depth to which the tree of possible moves is searched. A value of zero causes this function to just apply
        the `evaluator` to the current position and return the result.
    maximize
        Signals whether the function should choose branches that maximize or minimize the evaluation score. By
        convention positive values are advantageous for white and negative values are advantageous for black. If white
        is to move, set this to `True`. (TODO read that from the `board`)

    Returns
    -------
    float
        Evaluation score of the current position in centi pawns.
    """

    if depth <= 0:
        return evaluator.eval(board)

    if board.is_checkmate():
        return -10_000 if board.turn == chess.WHITE else 10_000

    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    best_value = None
    if maximize:
        best_value = -99_999

        for move in board.legal_moves:
            board.push(move)
            best_value = max(
                best_value, minimax(board, evaluator, depth - 1, not maximize)
            )
            board.pop()
    else:
        best_value = 99_999

        for move in board.legal_moves:
            board.push(move)
            best_value = min(
                best_value, minimax(board, evaluator, depth - 1, not maximize)
            )
            board.pop()

    return best_value


# pylint: disable=too-many-arguments,too-many-branches
def cached_alpha_beta_search(
    board: chess.Board,
    evaluator: Evaluator,
    cache: ChessCache,
    depth: int,
    alpha: float,
    beta: float,
) -> float:
    """Cached variant of the :func:`alpha_beta_search` algorithm"""

    if depth <= 0:
        value = None
        if cache.contains(board, depth):
            value = cache.get_value(board)
        else:
            value = evaluator.eval(board)
            cache.insert_or_update(board, depth, value)
        return value

    if board.is_checkmate():
        return -10_000 if board.turn == chess.WHITE else 10_000

    best_value = None
    if board.turn == chess.WHITE:
        best_value = -99_999

        for move in board.legal_moves:
            board.push(move)

            search_value = None
            if cache.contains(board, depth - 1):
                search_value = cache.get_value(board)
            else:
                search_value = alpha_beta_search(board, evaluator, depth - 1, alpha, beta)
                cache.insert_or_update(board, depth, search_value)

            best_value = max(best_value, search_value)

            board.pop()

            alpha = max(alpha, best_value)
            if alpha >= beta:
                break
    else:
        best_value = 99_999

        for move in board.legal_moves:
            board.push(move)

            search_value = None
            if cache.contains(board, depth - 1):
                search_value = cache.get_value(board)
            else:
                search_value = alpha_beta_search(board, evaluator, depth - 1, alpha, beta)
                cache.insert_or_update(board, depth, search_value)

            best_value = min(best_value, search_value)

            board.pop()

            beta = min(beta, best_value)
            if beta <= alpha:
                break

    return best_value


# pylint: disable=too-many-arguments
def alpha_beta_search(
    board: chess.Board,
    evaluator: Evaluator,
    depth: int,
    alpha: float,
    beta: float,
) -> float:
    """Alpha-Beta algorithm for search-based evaluation of a chess position

    Parameters
    ----------
    board
        State of the chess board to be evaluated
    evaluator
        Evaluation function used at leaf nodes
    depth
        The depth to which the tree of possible moves is searched. A value of zero causes this function to just apply
        the `evaluator` to the current position and return the result.
    alpha
        Parameter for tree pruning. Use large negative value to initialize the algorithm.
    beta
        Parameter for tree pruning. Use large positive value to initialize the algorithm.

    Returns
    -------
    float
        Evaluation score of the current position in centi pawns.
    """

    if depth <= 0:
        return evaluator.eval(board)

    if board.is_checkmate():
        return -10_000 if board.turn == chess.WHITE else 10_000

    best_value = None
    if board.turn == chess.WHITE:
        best_value = -99_999

        for move in board.legal_moves:
            board.push(move)
            best_value = max(
                best_value,
                alpha_beta_search(board, evaluator, depth - 1, alpha, beta),
            )
            board.pop()

            alpha = max(alpha, best_value)
            if alpha >= beta:
                break
    else:
        best_value = 99_999

        for move in board.legal_moves:
            board.push(move)
            best_value = min(
                best_value,
                alpha_beta_search(board, evaluator, depth - 1, alpha, beta),
            )
            board.pop()

            beta = min(beta, best_value)
            if beta <= alpha:
                break

    return best_value
