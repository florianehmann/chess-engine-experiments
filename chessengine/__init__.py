"""Tools and algorithms for implementing a chess engine."""

import chess

from .searchers import Searcher, SearchResult


def get_next_move(board: chess.Board, searcher: Searcher) -> tuple[chess.Move, SearchResult]:
    """Find the best next move for the current position of `board` using the provided `searcher`."""
    return searcher.search(board).moves[0]
