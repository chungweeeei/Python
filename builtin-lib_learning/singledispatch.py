from functools import (
    singledispatch,
    singledispatchmethod
)

def func_without_singledispatch(args):
    
    if isinstance(args, int):
        print("[func_without_singledispatch] Got an int: {}".format(args))
    elif isinstance(args, float):
        print("[func_without_singledispatch] Got an float: {}".format(args))
    elif isinstance(args, list):
        print("[func_without_singledispatch] Got an list: {}".format(args))
    elif isinstance(args, dict):
        print("[func_without_singledispatch] Got an dict: {}".format(args))

@singledispatch
def func(args):
    print("[func] Got something: {}".format(args))

@func.register
def _int(args: int):
    print("[func] Got an int: {}".format(args))

@func.register
def _list(args: list):
    print("[func] Got an list: {}".format(args))

'''
    NOTE
    For functions annotated with types, the decorator will infer the type of the first argument automatically.

    after 3.11 version singledispatch support types.UnionType and typing.Union.
    
    we can also use singledispatchmethod in a class object
'''

class Negator:
    
    @singledispatchmethod
    def neg(self, arg):
        raise NotImplementedError("Cannot negate a")

    @neg.register
    def _int(self, args: int):
        return -args

    @neg.register
    def _float(self, args: float):
        return -args

'''
    NOTE
    singledispatchmethod can use with other decorator
'''

class TestNegator:
    
    @singledispatchmethod
    @classmethod
    def neg(cls, arg):
        raise NotImplementedError("Cannot negate a")

    @neg.register
    @classmethod
    def _int(cls, args: int):
        return -args

    @neg.register
    @classmethod
    def _float(cls, args: float):
        return -args


if __name__ == "__main__":
    
    func_without_singledispatch(args=5)
    func_without_singledispatch(args=0.99)
    func_without_singledispatch(args=[1, 2, 3])
    func_without_singledispatch(args={"test": [1, 2, 3]})
    
    func(123)
    func([1, 2, 3])
    func({"test": [1, 2, 3]})
    
    negator = Negator()

    resp = negator.neg(5)
    print("[Negator] int resp: {}".format(resp))
    
    resp = negator.neg(2.7)
    print("[Negator] float resp: {}".format(resp))
    
    try: 
        resp = negator.neg([1, 2, 3])
    except Exception as e:
        print("[Negator] ERROR: {}".format(e))
    
    '''
        NOTE 
        more detail aboue classmethod
    '''

    test_neg_func = TestNegator.neg
    resp = test_neg_func(5)
    print("[TestNegator] int resp: {}".format(resp))
    
    resp = test_neg_func(2.7)
    print("[TestNegator] float resp: {}".format(resp))
    
    try: 
        resp = test_neg_func([1, 2, 3])
    except Exception as e:
        print("[TestNegator] ERROR: {}".format(e))