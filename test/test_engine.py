#!/usr/bin/env python3

# r2qrk2/pp3p2/2pb1nn1/5Np1/3P4/7Q/PP4PP/R4RK1 w Qq - 0 1

import sys
import os

parent = os.path.basename(os.getcwd())
if parent == 'test':
  sys.path.insert(0, '../koksszachy')
if parent == 'KoksSzachy':
  sys.path.insert(0, 'koksszachy')
from engine import KoksSzachy

import unittest

class TestEngine(unittest.TestCase):
  def test_eval(self):
    a = KoksSzachy("r1b2k1r/pp1pQppp/3P4/5P2/8/5N2/4KP1P/qN3B1R b - - 3 19")
    b = KoksSzachy("r1b2k1r/pp1pQppp/3P4/5P2/8/5N2/4KP1P/qN3B1R b - - 3 19")
    ma = a.iter_deep(5)
    mb = b.iter_deep(5)
    # warto zauwazyc, ze wprowadzjąc zmiany w algorytmie minimaxu ten ruch może być inny.
    assert(str(ma) == 'f8g8' == str(mb)) 
    del a,b,ma,mb

  # force checkmates, byl z tym pewien problem. opisane w #17

  def test_eval_complex(self):
    a = KoksSzachy("4k3/8/2N1Q1P1/pr2P3/8/1P3P2/1K5P/8 b - - 2 48")
    b = KoksSzachy("4k3/8/2N1Q1P1/pr2P3/8/1P3P2/1K5P/8 b - - 2 48")
    ma = a.iter_deep(5)
    mb = b.iter_deep(5)
    # warto zauwazyc, ze wprowadzjąc zmiany w algorytmie minimaxu ten ruch może być inny.
    assert(str(ma) == 'e8f8' == str(mb)) 
    #del ma,mb
    a.game.push(ma)
    b.game.push(mb)
    del ma,mb
    ma = a.iter_deep(5)
    mb = b.iter_deep(5)
    assert(str(ma) == 'e6f7' == str(mb)) 

  def test_eval_complex1(self):
    a = KoksSzachy("r1br2k1/ppp2ppQ/5p2/8/8/8/PPP2PPR/R1B1KBN1 b Q - 0 11")
    b = KoksSzachy("r1br2k1/ppp2ppQ/5p2/8/8/8/PPP2PPR/R1B1KBN1 b Q - 0 11")
    ma = a.iter_deep(5)
    mb = b.iter_deep(5)
    # warto zauwazyc, ze wprowadzjąc zmiany w algorytmie minimaxu ten ruch może być inny.
    assert(str(ma) == 'g8f8' == str(mb)) 
    del ma,mb,a,b

if __name__ == '__main__':
  unittest.main()
