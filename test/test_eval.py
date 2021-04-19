#!/usr/bin/env python3

import unittest
from ..koksszachy.engine import KoksSzachy
import chess

class TestEval(self):
  def test_eval(self):
    self.assertEqual(KoksSzachy.evaluate(), value, 'Should be {value}')

if __name__=="__main__":
  unittest.main()
