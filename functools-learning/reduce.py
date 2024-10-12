import time
import functools

'''
    NOTE:
    functools.reduce(function, iterable[, initializer])
    
    reduce is a function not a decorator. 
    
    Apply function of two arguments cumulatively to the items of iterable, from left to right, so as to reduce the iterable to a single value
'''

def sum_from_one_to_five():
    
    total = 0
    for i in range(5):
        total += i
        
    print("[sum_from_one_to_five] total: {}".format(total)) 

def sum_from_one_to_five_use_reduct():
    
    # nums is a iterable object
    nums = [i for i in range(5)]

    started_at = time.time()
    sum(nums)
    print("[sum_from_one_to_five_use_reduct] it tasks {}sec when using sum function".format(time.time() - started_at))

    started_at = time.time()
    total = functools.reduce(lambda x, y: x + y, nums)
    print("[sum_from_one_to_five_use_reduct] it tasks {}sec when using reduce function".format(time.time() - started_at))

    '''
        the mechanism behind reduce can be displayed below:
        
        ((((0 + 1) + 2) + 3) + 4)
        
        pros:
            make program clean and readable.
        
        cons:
            the performance of reduce function is worse than sum() function or for loop.
    '''
    
    print("[sum_from_one_to_five_use_reduct] total: {}".format(total))

'''
    reduce roughly equivalent to:
    
    def reduce(function, iterable, initializer=None):
        it = itera(iterable)
        
        if initializer is None:
            value = next(it)
        else:
            value = initializer
        
        for element in it:
            value = function(value, element)
            
        return value
'''

if __name__ == "__main__":
    
    sum_from_one_to_five()
    sum_from_one_to_five_use_reduct()
    
    '''
        NOTE
        we can take a look for itertools.accumulate function.
    '''