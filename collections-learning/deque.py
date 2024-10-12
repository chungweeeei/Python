from collections import deque

if __name__ == "__main__":
    
    d = deque("ghi")
    for elem in d:
        print("elem: {}".format(elem.upper()))
        
    d.append("j")
    print("{}".format(d))
    
    d.appendleft("f")
    print("{}".format(d))
    
    print("number of g in deque: {}".format(d.count("g")))
    
    d.extend("klm")
    print("{}".format(d))
    
    d.extendleft("cde")
    print("{}".format(d))
    
    d.insert(1, "z")
    print("{}".format(d))
    
    d.pop()
    print("{}".format(d))
    
    d.popleft()
    print("{}".format(d))
    
    d.remove("g")
    print("{}".format(d))
    
    d.reverse()
    print("{}".format(d))
    
    d.rotate(1)
    print("{}".format(d))
    
    d.rotate(-1)
    print("{}".format(d))
    
    d.clear()
    print("{}".format(d))