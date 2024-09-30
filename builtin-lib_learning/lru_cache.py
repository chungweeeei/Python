from functools import lru_cache
from dataclasses import dataclass

'''
    low-level implementaion of cache actually is used lru_cache. 
    
    @cache is equal to @lru_cache(maxsize=None). 
    
    The default maxsize of lru_cache is 128.
'''

@lru_cache(maxsize=32)
def fabonacci(n: int) -> int:
    
    if n < 1:
        return 0
    elif n == 1:
        return 1
    
    return fabonacci(n - 1) + fabonacci(n - 2)

@lru_cache()
def say(word: str, times: int = 1, end="\n"):
    for _ in range(times):
        print(word, end=end)

if __name__ == "__main__":

    fabonacci(n=20)
    
    '''
        NOTE 
        if you want to check cache operation status, you can use cache_info function.
    '''

    print(fabonacci.cache_info())
    # cache_info => CacheInfo(hits=18, misses=21, maxsize=32, currsize=21)

    '''
        NOTE
        Two points to note when using caching-related decorators from functools.
        
        1. The order of the arguments in cached function.
        
        For example Although the following two calls say(word="Hi", times=1, end="\n") and say(word="Hi", end="\n", times=1) produce the same result, due to the different parameter positions, they will cause cache two miss. 
    '''
    
    say(word="Hi", times=1, end="\n")
    print(say.cache_info())
    
    say(word="Hi", end="\n", times=1)
    print(say.cache_info())
    
    # directly get result from im-memory cache
    say(word="Hi", times=1, end="\n")
    print(say.cache_info())
    
    '''
        2. The arguments in the cached functio must be hashable.
    '''
    
    @dataclass(frozen=True)
    class User:
        id: int
        name: str

    @lru_cache
    def query_user_txs(user: User):
        pass
    
    '''
        User object is not hashable, so we get this error [TypeError: unhashable type: 'User']

        if we want to fix the issue, we can just simply set dataclass to frozen dataclass
    ''' 
    
    query_user_txs(user=User(1, "Test"))