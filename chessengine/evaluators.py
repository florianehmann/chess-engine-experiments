"""Position evaluation functions"""

from abc import ABC, abstractmethod

import chess


# pylint: disable=too-few-public-methods
class Evaluator(ABC):
    """Function to evaluate a given chess position"""
    @abstractmethod
    def eval(self, board: chess.Board) -> float:
        """Takes the current position of `board` and returns an evaluation score in centi pawns"""


class SimpleEvaluator(Evaluator):
    """Simple hand-crafted evaluation function based on static piece-values and positional bonuses and penalties"""

    PIECE_SQUARE_TABLE = [
        [ -50 , -40 , -30 , -30 , -30 , -30 , -40 , -50],
        [ -40 , -20 ,   0 ,   0 ,   0 ,   0 , -20 , -40],
        [ -30 ,   0 ,  10 ,  15 ,  15 ,  10 ,   0 , -30],
        [ -30 ,   5 ,  15 ,  20 ,  20 ,  15 ,   5 , -30],
        [ -30 ,   0 ,  15 ,  20 ,  20 ,  15 ,   0 , -30],
        [ -30 ,   5 ,  10 ,  15 ,  15 ,  10 ,   5 , -30],
        [ -40 , -20 ,   0 ,   5 ,   5 ,   0 , -20 , -40],
        [ -50 , -40 , -30 , -30 , -30 , -30 , -40 , -50]
    ]

    PIECE_VALUES = {
        chess.PAWN:   100,
        chess.KNIGHT: 310,
        chess.BISHOP: 320,
        chess.ROOK:   500,
        chess.QUEEN:  900,
    }

    def eval(self, board: chess.Board):
        scores = {chess.WHITE: 0, chess.BLACK: 0}

        for square in chess.SQUARES:
            piece = board.piece_at(square)

            if piece is None or piece.piece_type == chess.KING:
                continue

            scores[piece.color] += (
                self.PIECE_VALUES[piece.piece_type]
                + self.PIECE_SQUARE_TABLE[chess.square_file(square)][chess.square_rank(square)]
            )

        return scores[chess.WHITE] - scores[chess.BLACK]
