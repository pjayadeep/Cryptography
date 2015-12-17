from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor
import inspect

def func(x, y):
	'Some function. Nothing too interesting'
	import time
	time.sleep(5)
	return x + y

def inlined_future(func):
    assert inspect.isgeneratorfunction(func)
    return func

def run_inline_future(fut):
    t  = start_inline_future(fut)
    return t.result()

@inlined_future
def do_func(x, y):
	result = yield pool.submit(func, x, y)
	print('Got:', result)

run_inline_future(do_func)
