#!/usr/bin/env python3

import unittest
import chess
from koksszachy.engine import KoksSzachy


"""
rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR%20b%20KQkq%20e3%200%201

rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1
"""

class TestEval(unittest.TestCase):
  def test_eval(self):
    v = KoksSzachy("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
    val = v.evaluate()
    #print(val)
    self.assertEqual(val, (0,10))


if __name__=="__main__":
  unittest.main()
