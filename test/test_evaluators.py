"""Test evaluators"""

import chess
import pytest

from chessengine.evaluators import SimpleHandCraftedEvaluator, SimpleEvaluator

from .chess_test_data import fens


@pytest.mark.parametrize("fen_key,score", [
    ("starting", 0),
    ("london", 0),
    ("random-nonsense", -1500)
])
def test_simple_evaluator(fen_key, score):
    """Test simple piece counting on a few examples"""
    evaluator = SimpleEvaluator()
    evaluation = evaluator.eval(chess.Board(fens[fen_key]))
    assert evaluation == score


@pytest.mark.parametrize("fen_key,score", [
    ("starting", 0),
    ("london", 25),
    ("random-nonsense", -1415)
])
def test_simple_hand_crafted_evaluator(fen_key, score):
    """Test a simple hand-crafted evaluation function on a few examples"""
    evaluator = SimpleHandCraftedEvaluator()
    evaluation = evaluator.eval(chess.Board(fens[fen_key]))
    assert evaluation == score
