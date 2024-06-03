"""Test evaluators"""

import chess
import pytest

from chessengine.evaluators import SimpleHandCraftedEvaluator, SimpleEvaluator

fens = {
    "starting": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "london": "r1bqk2r/p1p2p1p/2n1pn2/1pbp2p1/3P1B2/2PBPN2/PP1N1PPP/R2Q1RK1 b kq - 1 8",
    "random-nonsense": "r3kbnr/pp3ppp/2n5/8/4PP2/2q5/PPPB2PP/3bKBNR w Kkq - 0 10",
}


@pytest.mark.parametrize("fen,score", [
    (fens["starting"], 0),
    (fens["london"], 0),
    (fens["random-nonsense"], -1500)
])
def test_simple_evaluator(fen, score):
    """Test simple piece counting on a few examples"""
    evaluator = SimpleEvaluator()
    evaluation = evaluator.eval(chess.Board(fen))
    assert evaluation == score


@pytest.mark.parametrize("fen,score", [
    (fens["starting"], 0),
    (fens["london"], 25),
    (fens["random-nonsense"], -1415)
])
def test_simple_hand_crafted_evaluator(fen, score):
    """Test a simple hand-crafted evaluation function on a few examples"""
    evaluator = SimpleHandCraftedEvaluator()
    evaluation = evaluator.eval(chess.Board(fen))
    assert evaluation == score
