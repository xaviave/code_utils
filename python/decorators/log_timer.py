import functools
import logging
import time


def timer(func):
    """
    Calculate and log the function execution time

    Parameters
    ----------
    func: function that will be executed. Given by python. no need to provide

    Examples
    --------

    @timer
    def calculate_something(n):
        result = n

        for x in range(n):
            n = n ** x

    def main():
        calculate_something(10)
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        value = func(*args, **kwargs)
        logging.info(f"{func.__name__!r} finished in {time.perf_counter() - start:.4f} secs")
        return value

    return wrapper
