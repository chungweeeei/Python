from collections import Counter

if __name__ == "__main__":
    
    # constrcut a empty Counter
    cnt = Counter()
    print("new counter: {}".format(cnt))
    
    # contruct with an iterable object(str)
    cnt = Counter("gallahad")
    print("counter with string object: {}".format(cnt))

    # contruct with an iterable object(dict)
    cnt = Counter({"red": 4, "blue": 2})
    print("counter with dict object: {}".format(cnt))

    # contruct with an iterable object(list)
    cnt = Counter(["eggs", "ham"])
    print("counter with list object: {}".format(cnt))

    # contruct with an keyword args
    cnt = Counter(cats=4, dogs=8)
    print("counter with keyword args: {}".format(cnt))
    
    cnt["elephant"] = 0
    print("cnt: {}".format(cnt))
    
    # remove element in Counter => use del (same as dict)
    del cnt["elephant"]
    
    # elements function return all elements in Counter
    print(list(cnt.elements()))
    
    # return a list of the n most common elements
    print(cnt.most_common(2))
    
    # Compute the sum of the counts.
    print(cnt.total())
    
    cnt.update({"elephant": 4})

    print(cnt)
    
    cnt.update({"elephant": 8})
    
    print(cnt)
    
    # clear Counter
    cnt.clear()
    
    print(cnt)
    
    # operatrion of Counter
    
    cnt1 = Counter(a=3, b=1)
    cnt2 = Counter(a=1, b=2)
    
    print(cnt1 + cnt2)      # add two counters together:  c[x] + d[x]
    print(cnt1 - cnt2)      # subtract (keeping only positive counts)
    print(cnt1 & cnt2)      # intersection:  min(c[x], d[x])
    print(cnt1 | cnt2)      # union:  max(c[x], d[x])
    print(cnt1 == cnt2)     # equality:  c[x] == d[x]