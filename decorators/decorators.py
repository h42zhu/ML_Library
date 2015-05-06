# a library for decorators
import time

def time_count_dec(func):

  def wrapper(*arg):
      t = time.clock()
      res = func(*arg)
      print func.func_name, time.clock()-t
      return res

  return wrapper

