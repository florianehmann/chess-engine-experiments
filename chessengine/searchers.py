"""Move tree searching functions"""

from abc import ABC, abstractmethod

import chess

from .evaluators import Evaluator


class Searcher(ABC):
    @abstractmethod
    def search(self, board: chess.Board) -> float:
        pass


class MinimaxSearcher(Searcher):

    def __init__(self, evaluator: Evaluator, depth: int):
        assert depth > 0

        self.evaluator = evaluator
        self.depth = depth

    def search(self, board: chess.Board) -> float:
        return minimax(board, self.evaluator, self.depth, board.turn == chess.WHITE)


class AlphaBetaSearcher(Searcher):

    def __init__(
        self,
        evaluator: Evaluator,
        depth: int,
        alpha: float = -1_000_000,
        beta: float = +1_000_000,
    ):
        assert depth > 0

        self.evaluator = evaluator
        self.depth = depth
        self.alpha = alpha
        self.beta = beta

    def search(self, board: chess.Board) -> float:
        return alpha_beta_search(board, self.evaluator, self.depth, self.alpha, self.beta)


def minimax(
    board: chess.Board, evaluator: Evaluator, depth: int, maximize: bool
) -> float:

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


def alpha_beta_search(
    board: chess.Board,
    evaluator: Evaluator,
    depth: int,
    alpha: float,
    beta: float,
) -> tuple[chess.Move, float]:

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
