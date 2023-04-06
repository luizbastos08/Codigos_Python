from time import time
from functools import wraps

def _timer(func):
    """
    Decorator that times each solution
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        solution = func(*args, **kwargs)
        end = time()
        solution['elapsed_time'] = end - start
        return solution

    return wrapper