# type your code below

def hello_world():
  print('Hello world')
  
hello_world()

for i in range(50):
  if i % 3 == 0 and i % 5 == 0:
    print('fizz')
  elif i % 3 == 0:
    print('buzz')
  else:
    print('fizzbuzz')