# {NOTE} https://stackoverflow.com/questions/1132941/least-astonishment-and-the-mutable-default-argument
'''
[Python] binds the default argument at function definition, and not at funtion execution.

From Python officially document: The default value is evaluated only once
'''

def foo_with_default_list(a, L=[]):
    L.append(a)
    return L

'''
If you don’t want the default to be shared between subsequent calls, you can write the function like this.
'''

def foo_with_default_None(a, L=None):
    if L is None:
        L = []
    L.append(a)
    return L

if __name__ == "__main__":
    
    print(foo_with_default_list(a=1))
    print(foo_with_default_list(a=2))
    print(foo_with_default_list(a=3))
    
    '''
        output will be:
        [1]
        [1, 2]
        [1, 2, 3]
    '''
    
    
    print(foo_with_default_None(a=1))
    print(foo_with_default_None(a=2))
    print(foo_with_default_None(a=3))

    '''
        output will be:
        [1]
        [2]
        [3]
    '''
    
    