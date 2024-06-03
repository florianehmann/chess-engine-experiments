"""Caching evaluation results"""

from dataclasses import dataclass

from cachetools import LRUCache
import chess


@dataclass
class CacheEntry:
    """Entries of the chess cache"""
    depth: int
    value: float


class ChessCache:
    """Cache for search-enhanced evaluations of positions"""

    def __init__(self, maxsize):
        self.cache = LRUCache(maxsize=maxsize)
        self.hits = 0
        self.misses = 0

    def contains(self, board: chess.Board, depth: int) -> bool:
        """Checks if board is present in cache with at least the specified depth"""
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