"""Move tree searching functions"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from cachetools import LRUCache
import chess

from .evaluators import Evaluator


@dataclass
class CacheEntry:
    """Entries of the cess cache."""
    depth: int
    value: float


class ChessCache:
    """Cache for search-enhanced evaluations of positions."""

    def __init__(self, maxsize):
        self.cache = LRUCache(maxsize=maxsize)
        self.hits = 0
        self.misses = 0

    def contains(self, board: chess.Board, depth: int) -> bool:
        """Checks if board is present in cache with at least the specified depth."""
        key = self.get_cache_key(board)

        if key not in self.cache:
            self.misses += 1
            return False

        entry = self.cache[key]
        if entry.depth < depth:
            self.misses += 1
            return False

        self.hits += 1
        return True

    def insert_or_update(self, board: chess.Board, depth: int, value: float) -> None:
        """Inserts the given board and depth into the cache.
        
        Overwrites if there already is an entry at the key generated from the board, regardless of
        depth."""

        key = self.get_cache_key(board)
        entry = CacheEntry(depth=depth, value=value)
        self.cache[key] = entry

    def get_value(self, board: chess.Board) -> float:
        """Retrieves the value of the board from cache at whatever depth it is stored."""

        return self.cache[self.get_cache_key(board)].value

    @staticmethod
    def get_cache_key(board: chess.Board) -> str:
        """Constructs a cache key from a board state.

        Currently, that includes the piece placement, active color, castling availability, and en passant square, i.e.,
        the first four entries of the FEN. The half move clock is omitted, because it probably doesn't become relevant
        enough often enough to matter in caching."""

        return " ".join(board.fen().split(" ")[:4])


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
        assert depth > 0
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
    """Cached variant of the :func:'~alpha_beta_search' algorithm"""

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
