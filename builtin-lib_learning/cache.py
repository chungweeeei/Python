import time
from functools import cache

'''
    NOTE:
    the functools module is for higher-order functions.
    any callable object can be treated as a function for the purpose of this module.
'''

'''
    cache decorator
    For some frequently called functions, if the same input values always produce the same output,
    it is quite suitable to use @cache to store the results.
    This can effectively improve program performances.
    below is an example of Fibonacci
'''

def fibonacci_without_cached(n: int) -> int:
    
    if n < 1:
        return 0
    elif n == 1:
        return 1 
    
    return fibonacci_without_cached(n - 1) + fibonacci_without_cached(n - 2)

@cache
def fibonacci_with_cached(n: int) -> int:
    
    if n < 1:
        return 0
    elif n == 1:
        return 1 
    
    return fibonacci_with_cached(n - 1) + fibonacci_with_cached(n - 2)

@cache
def factorial_with_cached(n: int) -> int:
    return n * factorial_with_cached(n - 1) if n else 1 

if __name__ == "__main__":
    
    started_at = time.time()
    fibonacci_without_cached(20)
    print("Takes {} to calculate fabonacci_without_cached(20)".format(time.time() - started_at))
    
    started_at = time.time()
    fibonacci_with_cached(20)
    print("Takes {} to calculate fibonacci_with_cached(20)".format(time.time() - started_at))
    
    
    '''
        NOTE:
        It took around 0.0157 seconds to obtain result when calling fabonacci_without_cached function. However, 
        it took around 0.00022 seconds to obtain result when calling fibonacci_with_cached function.
        
        Why these two functions have this big difference. The reason is that fibonacci_with_cached store all the values that 
        has been calculated. So fibonacci_with_cached(20) directly take values of fibonacci_with_cached(19) and fibonacci_with_cached(18) from memory.
    '''
    
    factorial_with_cached(n=20) # no previously cached result, make 21 recursive calls
    factorial_with_cached(n=10) # just looks up cached value result
    factorial_with_cached(n=22) # makes two new recursive calls, the other 10 are cached
    
    '''
        The cache is threadsafe so the wrapped function can be used in multiple threads.
        
        ! remeber cache decorator should run after Python 3.9 version
    '''
    