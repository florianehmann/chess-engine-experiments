from abc import ABC, abstractmethod
from enum import auto, Enum
from functools import total_ordering
from typing import Self

import chess


class SearchResultType(Enum):
    """What type of result the searcher has found"""
    SCORE = auto()
    """The search returns a regular evaluation score."""
    MATE = auto()
    """The search determines that there is a guaranteed mate in a number of moves for the current color."""
    DRAW = auto()
    """The search ends in a draw."""


# pylint: disable=attribute-defined-outside-init
@total_ordering
class SearchResult:
    """Result of a search into the move tree.

    This class cannot be instantiated directly but is constructed in the factory methods :meth:`from_score` and
    :meth:`from_mate`, depending on the :class:`SearchResultType` of the result.
    """

    def __init__(self):
        # put those here so IDE/linter recognize them
        self.moves: list[chess.Move] = []
        self.score: float | None = None
        self.type: SearchResultType | None = None
        self.winner: bool | None = None

        raise TypeError("SearchResult cannot be instantiated directly, use factory methods")

    def __new__(cls):
        return super().__new__(cls)
    
    def __repr__(self):
        type_part = self.type
        if self.type == SearchResultType.SCORE:
            type_part = f"score={self.score}"
        return f"<SearchResult {type_part} move={self.moves}>"

    def __eq__(self, other: Self) -> bool:
        assert isinstance(other, self.__class__)

        # shorter mates are better
        if self.type == SearchResultType.MATE and other.type == SearchResultType.MATE:
            if len(self.moves) != len(other.moves):
                return False

        return self.get_effective_score() == other.get_effective_score()

    def __lt__(self, other: Self) -> bool:
        assert isinstance(other, self.__class__)

        # shorter mates are better
        if self.type == SearchResultType.MATE and other.type == SearchResultType.MATE:
            if self.winner == other.winner:
                if self.winner == chess.WHITE:
                    return len(self.moves) > len(other.moves)
                else:
                    return len(self.moves) < len(other.moves)

        return self.get_effective_score() < other.get_effective_score()

    def get_effective_score(self) -> float:
        """Get a score value for a result. Positive or negative infinity for mate and zero for draw."""
        if self.type == SearchResultType.SCORE:
            return self.score
        elif self.type == SearchResultType.MATE:
            return float("inf") if self.winner == chess.WHITE else float("-inf")
        else:
            return 0.0

    @classmethod
    def from_score(cls, score: float, moves: list[chess.Move]) -> Self:
        """Create a search result that represents a regular evaluation score."""

        instance = cls.__new__(cls)
        instance.type = SearchResultType.SCORE
        instance.moves = moves
        instance.score = score

        return instance

    @classmethod
    def from_mate(cls, winner: bool, moves: list[chess.Move]) -> Self:
        """Create a search result that represents forced mate in a certain number of moves."""

        instance = cls.__new__(cls)
        instance.type = SearchResultType.MATE
        instance.moves = moves
        instance.winner = winner

        return instance

    @classmethod
    def from_draw(cls, moves: list[chess.Move]) -> Self:
        """Create a search result that represents forced mate in a certain number of moves."""

        instance = cls.__new__(cls)
        instance.type = SearchResultType.DRAW
        instance.moves = moves

        return instance


# pylint: disable=too-few-public-methods
class Searcher(ABC):
    """Search algorithm that provides an evaluation of a chess position based on searching in the tree of
    possible moves"""
    @abstractmethod
    def search(self, board: chess.Board) -> SearchResult:
        """Performs the tree search and returns an evaluation in centi pawns"""
