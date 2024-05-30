"""Tests of the """

import chess
import pytest

from chessengine.searchers import SearchResult


def test_search_result_direct_instantiation():
    """It should be impossible to instantiate `SearchResult` directly."""
    with pytest.raises(TypeError):
        SearchResult()


def test_search_result_from_score():
    """It should be possible to create an instance of `SearchResult` from the `from_score` factory."""
    result = SearchResult.from_score(15.0)
    assert isinstance(result, SearchResult)


def test_search_result_from_mate():
    """It should be possible to create an instance of `SearchResult` from the `from_mate` factory."""
    result = SearchResult.from_mate([chess.Move.from_uci('a2a3')])
    assert isinstance(result, SearchResult)
