"""Move tree searching functions"""

from abc import ABC, abstractmethod
from enum import Enum, auto

import chess

from ..cache import ChessCache
from ..evaluators import Evaluator

from .abstract import Searcher, SearchResult
from .minimax_searcher import MinimaxSearcher


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
