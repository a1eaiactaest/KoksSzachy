#!/usr/bin/env python3
import sys
import os

parent = os.path.basename(os.getcwd())
if parent == 'test':
  sys.path.insert(0, '../koksszachy')
if parent == 'KoksSzachy':
  sys.path.insert(0, 'koksszachy')
from engine import KoksSzachy

import unittest
#from koksszachy.engine import KoksSzachy


"""
rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR%20b%20KQkq%20e3%200%201

rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1


przetestowac to:

5k2/4N3/4Q1P1/pr2P3/8/1P3P2/1K5P/8 b - - 0 47

"""

class TestEval(unittest.TestCase):
  def test_eval_basic(self):
    v = KoksSzachy("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
    val = v.evaluate()
    self.assertEqual(val, (0,10))

  def test_eval_1(self):
    v = KoksSzachy("1r4k1/p1p2ppp/8/8/q7/N7/5nPP/K3Q2R b - - 0 31")
    val = v.evaluate()
    self.assertEqual(val, (-300, -390))

  def test_eval_2(self):
    v = KoksSzachy("4r1k1/1p3ppp/p5N1/3p1R2/8/PPnn3b/8/K7 b - - 5 31")
    val = v.evaluate()
    self.assertEqual(val, (-1000, -1095))




if __name__=="__main__":
  unittest.main()
