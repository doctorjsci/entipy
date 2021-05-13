# этот тест проверяет, соответствует ли функция listcomp() требованиям

from examples.evaluation.listcomp import listcomp

def test_listcomp():
  assert len(listcomp()) == 8