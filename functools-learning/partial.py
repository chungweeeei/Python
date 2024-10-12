import functools
import requests

'''
    NOTE
    functools.partial(func, /, *args, **keywors)
    
    Return a new partial object which when called will behave like func called with the positional arguments args and keyword arguments keywords.
    
    This new partial object can be called just as a function, except that some arguments have aleady be assigned.
    
    below we use requests.get for an example.
'''

'''
    NOTE
    
    offically document: https://docs.python.org/zh-tw/3/library/functools.html
    
    low-level code of partial function

    def partial(func, /, *args, **keywords):
        def newfunc(*fargs, **fkeywords):
            newkeywords = {**keywords, **fkeywords}
            return func(*args, *fargs, **newkeywords)
        newfunc.func = func
        newfunc.args = args
        newfunc.keywords = keywords
        return newfunc
        
    above code is classical decorator syntex.
'''

def request_without_partial():
    
    resp = requests.get(url="https://httpbin.org/headers", 
                        headers={"User-Agent": "Chrome"})

    print("[request_withou_partial] {}".format(resp.json()))

def request_with_partial():
    
    '''
        We use partial function to wrapper request.get and headers argument together
        
        Therefore when we call this new function object, we just need to fill-in url.
    '''
    
    get = functools.partial(requests.get, headers={"User-Agent": "Chrome"})

    resp = get(url="https://httpbin.org/headers")
    
    print("[request_with_partial] {}".format(resp.json()))
    
def reqeust_with_multiple_partial():
    
    get = functools.partial(requests.get, headers={"User-Agent": "Chrome"})
    
    print("[reqeust_with_multiple_partial] {}".format(get))
    
    get = functools.partial(get, params={"param1": "p1"})
    
    print("[reqeust_with_multiple_partial] {}".format(get))
    
    '''
        keyword arguments already existed, then partial function will replace old arguments.
    '''
    
    get = functools.partial(get, params={"param2": "p2"})
    
    print("[reqeust_with_multiple_partial] {}".format(get))

if __name__ == "__main__":
    
    request_without_partial()
    request_with_partial()
    reqeust_with_multiple_partial()