from collections import namedtuple

if __name__ == "__main__":
    
    Point = namedtuple(typename='Point', field_names=['x', 'y', "x"], rename=True)
    p1 = Point(x=11, y=22, _2=10)

    p2 = p1._replace(x=10, y=23, _2=13)
    print("p1: {}".format(p1))
    print("p2: {}".format(p2))
    
    # p3 = tuple([11, 22])
    # print("p3: {}".format(p3))
    