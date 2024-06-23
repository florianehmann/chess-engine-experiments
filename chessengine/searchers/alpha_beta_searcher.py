import chess

from ..evaluators import Evaluator

from .abstract import Searcher


class AlphaBetaSearcher(Searcher):
    """Searcher based on Alpha-Beta Pruning"""

    def __init__(self, evaluator: Evaluator, depth: int):
        assert depth >= 0

        self.evaluator = evaluator
        self.depth = depth
        self.alpha = float("-inf")
        self.beta = float("inf")

    def search(self, board: chess.Board) -> float:
        return alpha_beta_search(board, self.evaluator, self.depth, self.alpha, self.beta)


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
