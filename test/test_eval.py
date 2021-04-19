#!/usr/bin/env python3

import time
import unittest
import requests
import threading
from tqdm import tqdm
from koksszachy import engine, play

def start_server():
  play.main('--play')

def check_server():
  src = requests.get('http://127.0.0.1:5000/').content
  if b'<title>KoksSzachy</title>' in src:
    print(src)
  
''' 
class UnitTest(unittest.TestCase):
  def test_server(self):
    server = threading.Thread(target=start_server)
'''

    

if __name__=="__main__":
  #unittest.main()
  #server = threading.Thread(target=start_server)
  check = threading.Thread(target=check_server)
  #server.start(), 
  check.start()
  time.sleep(5)
  check.join()

