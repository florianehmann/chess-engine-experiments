"""Tools and algorithms for implementing a chess engine."""

import chess

from .searchers import Searcher


def get_next_move(board: chess.Board, searcher: Searcher) -> tuple[chess.Move, float]:
    best_move = None
    best_value = -99_999

    if board.turn == chess.BLACK:
        best_value = 99_999

    for move in board.legal_moves:
        board.push(move)
        value = searcher.search(board)
        board.pop()

        if board.turn == chess.WHITE:
            if value > best_value:
                best_value = value
                best_move = move
        else:
            if value < best_value:
                best_value = value
                best_move = move

    return best_move, best_value
