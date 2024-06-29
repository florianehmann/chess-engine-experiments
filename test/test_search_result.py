"""Tests of the search result data type"""

import chess
import pytest

from chessengine.searchers import SearchResult, SearchResultType


def test_search_result_direct_instantiation():
    """It should be impossible to instantiate `SearchResult` directly."""
    with pytest.raises(TypeError):
        SearchResult()


def test_search_result_from_score():
    """It should be possible to create an instance of `SearchResult` from the `from_score` factory."""
    result = SearchResult.from_score(15.0, [])
    assert isinstance(result, SearchResult)


def test_search_result_from_mate():
    """It should be possible to create an instance of `SearchResult` from the `from_mate` factory."""
    result = SearchResult.from_mate(chess.WHITE, [])
    assert isinstance(result, SearchResult)


def test_search_result_from_draw():
    """It should be possible to create an instance of `SearchResult` from the `from_draw` factory."""
    result = SearchResult.from_draw([])
    assert isinstance(result, SearchResult)
    assert result.type == SearchResultType.DRAW


def test_search_result_equality():
    """Test if we can invoke the equality operator and get correct results"""
    score_result_1 = SearchResult.from_score(0.0, [])
    score_result_2 = SearchResult.from_score(0.0, [])

    assert score_result_1 == score_result_2


def test_search_result_ordering():
    """Test if comparison operators work"""
    score_result_white = SearchResult.from_score(1.0, [])
    score_result_black = SearchResult.from_score(-1.0, [])
    mate_result_white = SearchResult.from_mate(chess.WHITE, [])
    mate_result_black = SearchResult.from_mate(chess.BLACK, [])
    draw_result = SearchResult.from_draw([])

    assert score_result_white < mate_result_white
    assert mate_result_white > score_result_white
    assert draw_result < score_result_white
    assert score_result_black < draw_result
    assert mate_result_black < draw_result


def test_search_result_shorter_mates_better():
    """Test if a mate with the same winner but fewer moves is greater than another mate"""
    one_move = [chess.Move.null()]
    two_moves = [chess.Move.null(), chess.Move.null()]
    short_white_mate = SearchResult.from_mate(chess.WHITE, one_move)
    long_white_mate = SearchResult.from_mate(chess.WHITE, two_moves)
    short_black_mate = SearchResult.from_mate(chess.BLACK, one_move)
    long_black_mate = SearchResult.from_mate(chess.BLACK, two_moves)

    assert long_white_mate < short_white_mate
    assert short_black_mate < long_black_mate
