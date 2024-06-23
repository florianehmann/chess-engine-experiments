from abc import ABC, abstractmethod
from enum import auto, Enum

import chess


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
