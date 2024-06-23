"""Test Alpha-Beta searching algorithm"""

import chess
import pytest

from chessengine import evaluators, searchers

from .chess_test_data import fens


def test_instantiate():
    """Test if AlphaBetaSearcher can be instantiated"""
    evaluator = evaluators.SimpleEvaluator()
    searchers.AlphaBetaSearcher(evaluator, depth=0)


@pytest.mark.parametrize("fen_key", fens.keys())
def test_zero_depth_search(fen_key):
    """Test if the searcher returns the evaluator's scores at zero depth"""
    evaluator = evaluators.SimpleEvaluator()
    searcher = searchers.AlphaBetaSearcher(evaluator, depth=0)

    assert searcher.search(chess.Board(fens[fen_key])) == evaluator.eval(chess.Board(fens[fen_key]))


@pytest.mark.parametrize("fen_key,score", [
    ("starting", 0),
    ("london", 0),
    ("random-nonsense", -1500)
])
def test_shallow_search(fen_key, score):
    """Test if the search algorithm finds the expected scores for shallow search depths"""
    evaluator = evaluators.SimpleEvaluator()
    searcher = searchers.AlphaBetaSearcher(evaluator, depth=0)

    assert searcher.search(chess.Board(fens[fen_key])) == score


@pytest.mark.parametrize("fen_key,score", [
    ("starting", 0),
    ("london", -100),
    ("random-nonsense", -600)
])
def test_deeper_search(fen_key, score):
    """Test if the search algorithm finds the expected scores for slightly deeper search depths"""
    evaluator = evaluators.SimpleEvaluator()
    searcher = searchers.AlphaBetaSearcher(evaluator, depth=3)

    assert searcher.search(chess.Board(fens[fen_key])) == score
