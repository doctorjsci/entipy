# этот тест проверяет, соответствует ли функция listcomp() требованиям
import sys
sys.path.append('..')

from listcomp import listcomp

def test_listcomp():
  assert len(listcomp()) == 8