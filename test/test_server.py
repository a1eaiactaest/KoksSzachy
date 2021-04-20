#!/usr/bin/env python3

import sys
import requests
from multiprocessing import Process
from time import sleep
from koksszachy import play
import unittest


def check_server():
  #sleep(5)
  src = requests.get('http://localhost:5000').content
  ret_val = b'<title>KoksSzachy</title>' in src
  return ret_val 

def run_check():
  p1 = Process(target = play.main, args=('--play', False))
  p1.start()
  sleep(.1)
  ret = check_server()
  p1.terminate()
  p1.join()
  return ret
  

class TestServer(unittest.TestCase):
  def test_server(self):
    self.assertTrue(run_check())


if __name__ == "__main__":
  unittest.main()
